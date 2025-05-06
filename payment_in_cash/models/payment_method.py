from odoo import fields, models, api


class PaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['payment_cash'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res


