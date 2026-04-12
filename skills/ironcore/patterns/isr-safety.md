# Embedded Systems — ISR Safety Patterns

## Minimal Work in ISR (Deferred Processing)

```c
// ❌ BAD: Too much work in ISR blocks other interrupts
void USART1_IRQHandler_BAD(void) {
    char buffer[256]; int len = 0;
    while (USART1->SR & USART_SR_RXNE) buffer[len++] = USART1->DR;
    process_received_data(buffer, len);  // blocks!
    update_display();
    log_to_flash();
}

// ✅ GOOD: Defer processing to main loop
volatile uint8_t rx_buffer[256];
volatile uint8_t rx_count = 0;
volatile bool rx_complete  = false;

void USART1_IRQHandler(void) {
    if (USART1->SR & USART_SR_RXNE) {
        if (rx_count < sizeof(rx_buffer))
            rx_buffer[rx_count++] = USART1->DR;
    }
    if (USART1->SR & USART_SR_TC) {
        rx_complete = true;
        USART1->CR1 &= ~USART_CR1_TCIE;
    }
}

void main_loop(void) {
    if (rx_complete) {
        rx_complete = false;
        process_received_data(rx_buffer, rx_count);
        rx_count = 0;
    }
}
```

## Lock-Free Queue (SPSC)

```c
typedef struct {
    uint8_t buffer[QUEUE_SIZE];
    volatile uint32_t head;
    volatile uint32_t tail;
} LockFreeQueue;

bool queue_push(LockFreeQueue* q, uint8_t data) {
    uint32_t next_head = (q->head + 1) % QUEUE_SIZE;
    if (next_head == q->tail) return false;  // full
    q->buffer[q->head] = data;
    __DMB();                    // memory barrier before updating head
    q->head = next_head;
    return true;
}

bool queue_pop(LockFreeQueue* q, uint8_t* data) {
    if (q->head == q->tail) return false;  // empty
    *data = q->buffer[q->tail];
    __DMB();
    q->tail = (q->tail + 1) % QUEUE_SIZE;
    return true;
}
```

## Memory Barriers for ISR-Main Communication

```c
#define MEMORY_BARRIER() __DMB()  // Data Memory Barrier
#define MEMORY_FENCE()   __DSB()  // Data Synchronization Barrier

volatile bool     data_ready = false;  // MUST be volatile
volatile uint32_t data_value;

void ISR_Handler(void) {
    data_value = read_sensor();  // Write data first
    MEMORY_BARRIER();            // Ensure write completes
    data_ready = true;           // Then set flag
}

void main_loop(void) {
    if (data_ready) {
        MEMORY_BARRIER();               // Ensure flag read before data
        uint32_t value = data_value;    // Now safe to read
        data_ready = false;
        process_value(value);
    }
}
```
