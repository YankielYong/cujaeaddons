
SUPPORTED_CURRENCIES = (
    'EUR',
    'USD',
    'CUP',
)

PAYMENT_STATUS_MAPPING = {
    'pending': ('Pending',),
    'done': ('Processed', 'Completed'),
    'cancel': ('Voided', 'Expired'),
}
