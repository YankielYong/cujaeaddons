odoo.define('mx_elearning_plus.course_extended', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.websiteCourseExtended = publicWidget.Widget.extend({
        selector: '.o_course_extended',

        start: function () {
            var self = this;
            
            // Inicializar collapses con show
            $('.collapse.show').collapse('show');

            // Manejar clic en el botón
            this.$el.on('click', '#collapse_div', function(ev) {
                var $target = $($(this).data('target'));
                $target.collapse('toggle');
                
                // Actualizar ícono
                $(this).find('.fa')
                    .toggleClass('fa-plus fa-minus');
            });
        }
    });
});