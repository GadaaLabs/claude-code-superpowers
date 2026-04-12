# Embedded Systems — Hardware Abstraction Patterns

## Type-Safe Register Definitions

```c
// hardware/register_types.h
#define REG_BIT(pos)           (1U << (pos))
#define REG_MASK(width, pos)   (((1U << (width)) - 1) << (pos))
#define REG_GET(val, mask, pos) (((val) & (mask)) >> (pos))
#define REG_SET(val, mask, pos, field) (((val) & ~(mask)) | (((field) << (pos)) & (mask)))

typedef struct {
    volatile uint32_t MODER;   // Mode register
    volatile uint32_t OTYPER;  // Output type
    volatile uint32_t OSPEEDR; // Output speed
    volatile uint32_t PUPDR;   // Pull-up/pull-down
    volatile uint32_t IDR;     // Input data
    volatile uint32_t ODR;     // Output data
    volatile uint32_t BSRR;    // Bit set/reset
    volatile uint32_t AFR[2];  // Alternate function
} GPIO_TypeDef;

typedef enum { GPIO_MODE_INPUT=0, GPIO_MODE_OUTPUT=1, GPIO_MODE_AF=2, GPIO_MODE_ANALOG=3 } GPIO_Mode;

static inline void gpio_set_mode(GPIO_TypeDef* gpio, uint8_t pin, GPIO_Mode mode) {
    gpio->MODER = REG_SET(gpio->MODER, REG_MASK(2, pin*2), pin*2, mode);
}
static inline bool gpio_read(GPIO_TypeDef* gpio, uint8_t pin) {
    return (gpio->IDR & REG_BIT(pin)) != 0;
}
static inline void gpio_write(GPIO_TypeDef* gpio, uint8_t pin, bool value) {
    gpio->BSRR = value ? REG_BIT(pin) : REG_BIT(pin + 16);
}
```

## MMIO Safety

```c
/*
 * Rules: volatile for all registers, memory barriers after writes,
 * validate alignment, never dereference NULL or invalid addresses.
 */
static inline uint32_t mmio_read32(volatile uint32_t* addr) {
    if (!addr || ((uintptr_t)addr & 0x3)) return 0;  // NULL or misaligned
    return *addr;
}

static inline void mmio_write32(volatile uint32_t* addr, uint32_t value) {
    if (!addr) return;
    *addr = value;
    __DMB();  // Ensure write completes
}

bool mmio_validate_access(const MMIO_Region* region, uintptr_t offset, size_t size) {
    if (!region->base_address) return false;
    if (offset + size > region->region_size) {
        printf("MMIO OOB: %s offset=%zu size=%zu max=%zu\n",
               region->name, offset, size, region->region_size);
        return false;
    }
    return true;
}
```

## Endianness Handling

```c
#define BSWAP16(x) ((((x)&0x00FF)<<8) | (((x)&0xFF00)>>8))
#define BSWAP32(x) ((((x)&0x000000FF)<<24) | (((x)&0x0000FF00)<<8) | \
                    (((x)&0x00FF0000)>>8)  | (((x)&0xFF000000)>>24))

#if (*(const uint8_t*)"\x01\x02\x03\x04" == 0x04)  // little-endian
#define HTONS(x) BSWAP16(x)
#define HTONL(x) BSWAP32(x)
#define NTOHS(x) BSWAP16(x)
#define NTOHL(x) BSWAP32(x)
#else
#define HTONS(x) (x)
#define HTONL(x) (x)
#define NTOHS(x) (x)
#define NTOHL(x) (x)
#endif

// Safe network packet parsing
typedef struct {
    uint16_t length;    // Network byte order
    uint32_t sequence;  // Network byte order
    uint8_t data[];
} __attribute__((packed)) NetworkPacket;

void process_packet(const uint8_t* buffer, size_t size) {
    if (size < sizeof(NetworkPacket)) return;
    const NetworkPacket* pkt = (const NetworkPacket*)buffer;
    uint16_t length   = NTOHS(pkt->length);
    uint32_t sequence = NTOHL(pkt->sequence);
    if (length > size - sizeof(NetworkPacket)) return;  // truncated
    handle_packet(sequence, pkt->data, length);
}
```

## Timing Verification Checklist

```markdown
- [ ] Clock frequency within spec (target: ___ MHz, max: ___ MHz)
- [ ] Setup time verified (required: ___ ns, actual: ___ ns)
- [ ] Hold time verified (required: ___ ns, actual: ___ ns)
- [ ] Interrupt latency bounded (worst case: ___ cycles, budget: ___ cycles)
- [ ] DMA transfer complete before next trigger
- [ ] Watchdog timeout > max loop time (___ ms < ___ ms)
```
