var Utils = {
    urlQueryString: function(f, a, e, d) {
        if (null == a && (a = window.location.search), 0 == a.indexOf("?") && (a = a.substring(1, a.length)), null == e && (e = "&"), null == d && (d = "="), -1 != a.indexOf(f)) {
            for (var c = a.split(e), b = 0; b < c.length; b++)
                if (c[b].split(d)[0] == f) return c[b].substring(c[b].indexOf(d) + 1, c[b].length)
        }
        return null
    },
    loadXML: function(a, b, c) {
        $.get(a, function(a) {
            b(a, c)
        })
    },
    ajaxCommunication: function(a, b, c, d, e) {
        $.ajax({
            type: "POST",
            url: b,
            async: !1,
            data: a,
            contentType: "application/x-www-form-urlencoded",
            headers: e,
            success: function(a) {
                c(a, d)
            },
            error: function(b, d, a) {
                c(a)
            }
        })
    },
    getCount: function(a, c) {
        var b = 0;
        for (i = 0; i < a.length; i++) a[i] == c && b++;
        return b
    },
    getCountFromObject: function(a, c, d) {
        var b = 0;
        return $.each(a, function(e, a) {
            a[c] == d && b++
        }), b
    },
    stringify: function(a) {
        if (a instanceof Object) {
            var b = "";
            if (a.constructor === Array) {
                for (var c = 0; c < a.length; b += this.stringify(a[c]) + ",", c++);
                return "[" + b.substr(0, b.length - 1) + "]"
            }
            if (a.toString !== Object.prototype.toString) return '"' + a.toString().replace(/"/g, "\\$&") + '"';
            for (var d in a) b += '"' + d.replace(/"/g, "\\$&") + '":' + this.stringify(a[d]) + ",";
            return "{" + b.substr(0, b.length - 1) + "}"
        }
        return "string" == typeof a ? '"' + a.replace(/"/g, "\\$&") + '"' : String(a)
    },
    ruuid: function() {
        return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(b) {
            var a = 16 * Math.random() | 0;
            return ("x" == b ? a : 3 & a | 8).toString(16)
        })
    },
    formatelapsedTime: function(d) {
        var e = d % 3600,
            c = "" + (d - e) / 3600,
            a = "" + (d - 3600 * c - (e %= 60)) / 60,
            b = "" + Math.round(e);
        return "60" == b && (b = "00", a = "" + (a + 1)), c.length < 2 && (c = "0" + c), a.length < 2 && (a = "0" + a), b.length < 2 && (b = "0" + b), "PT" + c + "H" + a + "M" + b + "S"
    },
    checkDripFeed: async function(userEmail, courseId) {
        const querystring = `?email=${userEmail}&course=${courseId}`;
        Utils.getToken(querystring).then((data) => {
            result = $.get(`https://brainbot.ai/api/external/user-booster?token=${data}`, function(response, status) {
                let txt, title;
                if(parseInt(response.data.length) == 0) {
                    $('#dripfeed-button').removeClass('unsubscribe').addClass('subscribe');
                    title = 'Subscribe to Drip feed';
                } else {
                    $('#dripfeed-button').removeClass('subscribe').addClass('unsubscribe');
                    title = 'Unsubscribe to Drip feed';
                }
                $('#dripfeed-button').attr('title',title);
                $('#dripfeed-button').attr('original-title', title);
            });
            return result;
        });
    },
    getToken: async function(querystring) {
        result = await $.get(`../services/getToken.php${querystring}`, function(data, status){
			return data;
		});
        return result;
    },
    timeconversion: function(duration){
        const [hours, minutes, seconds] = duration.split(':');
        return parseFloat(Number(hours) * 60 * 60 + Number(minutes) * 60 + Number(seconds)).toFixed(1);
    },
    sortByKeyAscByName: function(array, key) {
        return array.sort(function (a, b) {
          var x = a[key];
          var y = b[key];
          return x < y ? -1 : x > y ? 1 : 0;
        });
      }
}