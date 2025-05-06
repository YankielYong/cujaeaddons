import json

from odoo import http
from odoo.http import request


class CashPaymentController(http.Controller):
    _accept_url = '/shop/payment/transaction'

    @http.route(_accept_url, type='http', auth='public', website=True, methods=['GET', 'POST'], csrf=False)
    def cash_return(self, **data):
        """ Simulate the response of a payment request.

        :param str reference: The reference of the transaction
        :param str customer_input: The payment method details
        :return: None
        """
        print(data)
        data.update({'payment_status': 'Completed'})

        request.env['payment.transaction'].sudo()._handle_notification_data('payment_cash', data)
        return request.redirect('/payment/status')








