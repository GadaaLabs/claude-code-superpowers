# Embedded Systems — RTOS Task Patterns

## Priority Assignment (Rate Monotonic Scheduling)

```c
/*
 * RMS: shorter period = higher priority
 * Utilization bound: U ≤ n(2^(1/n) - 1)
 * For n=3 tasks: U ≤ 0.78
 */
typedef struct {
    const char* name;
    uint32_t period_ms;
    uint32_t worst_case_ms;
    uint8_t priority;         // Higher number = higher priority
    void (*function)(void*);
} TaskConfig;

static const TaskConfig tasks[] = {
    {"Current_Loop",   100,  50,  3, task_current_control},
    {"Speed_Loop",     500, 100,  2, task_speed_control},
    {"Communication", 1000, 200,  1, task_handle_can},
};

void verify_schedulability(void) {
    float utilization = 0.0f;
    for (size_t i = 0; i < ARRAY_SIZE(tasks); i++)
        utilization += (float)tasks[i].worst_case_ms / tasks[i].period_ms;
    assert(utilization <= 0.78f && "System not schedulable under RMS");
}
```

## Stack Size Estimation (Watermark)

```c
#define STACK_PATTERN 0xA5
#define STACK_MARGIN  25    // 25% safety margin

void measure_stack_usage(TaskHandle_t task, uint8_t* stack_base, size_t stack_size) {
    memset(stack_base, STACK_PATTERN, stack_size);
    run_all_task_scenarios(task);

    size_t used = 0;
    for (size_t i = 0; i < stack_size; i++) {
        if (stack_base[i] != STACK_PATTERN) { used = stack_size - i; break; }
    }
    size_t required = used * (100 + STACK_MARGIN) / 100;
    printf("Task %s: used %zu B, recommend %zu B\n", task_name(task), used, required);
}
```

## IPC Mechanisms (FreeRTOS)

```c
// Queue for data transfer
TaskQueue* queue_create(size_t depth, size_t item_size) {
    TaskQueue* q = malloc(sizeof(TaskQueue));
    q->queue = xQueueCreate(depth, item_size);
    q->timeout_ms = pdMS_TO_TICKS(100);
    return q;
}

bool queue_send(TaskQueue* q, const void* data) {
    return xQueueSend(q->queue, data, q->timeout_ms) == pdPASS;
}

// Mutex with priority inheritance
Mutex* mutex_create(void) {
    Mutex* m = malloc(sizeof(Mutex));
    m->mutex = xSemaphoreCreateMutex();  // Has priority inheritance
    return m;
}
```

## Worst-Case Response Time (WCRT) Analysis

```c
/*
 * R_i = C_i + Σ⌈R_i/T_j⌉ * C_j  (all higher priority tasks j)
 * Iterate until convergence. If R_i > D_i → deadline missed.
 */
bool calculate_wcrt(TaskTiming* tasks, size_t count) {
    for (size_t i = 0; i < count; i++) {
        uint32_t response = tasks[i].wcet_ms, prev;
        do {
            prev = response;
            response = tasks[i].wcet_ms;
            for (size_t j = 0; j < i; j++)
                response += ((prev + tasks[j].period_ms - 1) / tasks[j].period_ms)
                            * tasks[j].wcet_ms;
        } while (response != prev);

        tasks[i].response_time = response;
        if (response > tasks[i].deadline_ms) {
            printf("Task %zu MISSES deadline: %u ms > %u ms\n",
                   i, response, tasks[i].deadline_ms);
            return false;
        }
    }
    return true;
}
```
