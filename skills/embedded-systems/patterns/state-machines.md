# Embedded Systems — State Machine Patterns

## Hierarchical State Machine (HSM)

```c
// state_machine/hsm.h
typedef struct State State;

struct State {
    const char* name;
    State* parent;
    void (*entry)(void);
    void (*exit)(void);
    bool (*handle_event)(uint32_t event, void* data);
};

typedef struct { State* current; void* context; } HSM;

#define TRANSITION(new_state) do { \
    if (hsm->current->exit)  hsm->current->exit(); \
    hsm->current = new_state; \
    if (hsm->current->entry) hsm->current->entry(); \
} while(0)
```

## State Transition Table

```c
typedef struct {
    State* from;
    uint32_t event;
    State* to;
    void (*action)(void);
} Transition;

// Example: traffic light controller
static const Transition transitions[] = {
    {&State_Red,    EVENT_TIMER_EXPIRED, &State_Green,  action_reset_timer},
    {&State_Green,  EVENT_TIMER_EXPIRED, &State_Yellow, action_reset_timer},
    {&State_Yellow, EVENT_TIMER_EXPIRED, &State_Red,    action_reset_timer},
    {&State_Red,    EVENT_EMERGENCY_VEH,&State_Green,  action_emergency_override},
};

State* get_next_state(State* current, uint32_t event) {
    for (size_t i = 0; i < ARRAY_SIZE(transitions); i++) {
        const Transition* t = &transitions[i];
        if (t->from == current && t->event == event) {
            if (t->action) t->action();
            return t->to;
        }
    }
    return current;  // No transition
}
```

## Guard Conditions

```c
typedef struct {
    State* from;
    uint32_t event;
    State* to;
    bool (*guard)(void);
    void (*action)(void);
} GuardedTransition;

static const GuardedTransition battery_transitions[] = {
    {
        .from   = &State_Charging,
        .event  = EVENT_TEMPERATURE_HIGH,
        .to     = &State_Cooling,
        .guard  = []() { return get_battery_temp() > TEMP_THRESHOLD; },
        .action = action_stop_charging,
    },
    {
        .from   = &State_Discharging,
        .event  = EVENT_LOW_BATTERY,
        .to     = &State_Shutdown,
        .guard  = []() { return get_battery_voltage() < VOLTAGE_MIN; },
        .action = action_save_and_shutdown,
    },
};
```

## State Machine Testing

```c
void test_transition_coverage(void) {
    State* states[] = {&State_Idle, &State_Running, &State_Error};
    uint32_t events[] = {EVENT_START, EVENT_STOP, EVENT_ERROR};

    for (size_t i = 0; i < ARRAY_SIZE(states); i++) {
        for (size_t j = 0; j < ARRAY_SIZE(events); j++) {
            bool handled = states[i]->handle_event(events[j], NULL);
            TEST_ASSERT_TRUE_MESSAGE(
                handled || states[i]->handle_event == default_handler,
                "State %s doesn't handle event %lu", states[i]->name, events[j]);
        }
    }
}

void test_no_unreachable_states(void) {
    // BFS/DFS from initial state to verify all states reachable
}
```
