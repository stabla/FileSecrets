function callPage() {
    setTimeout(function () {
        $aboutContainer.animate({
            left: "50%",
            width: "50%"
        }), $aboutMeTitle.show(), $blockIndex.show(), $("body").removeClass("hidden-before-load"), $("html").removeClass("hidden-before-load")
    }, 300), $(".mail-logo").on("click", function () {
        callContact(), $contactPage.addClass("active")
    }), $(".block--contact .close").on("click", function () {
        $contactPage.removeClass("active"), existProjects()
    }), $(".project-logo").on("click", function () {
        callProjects(), $projectsPart.addClass("active")
    }), $(".block--projects .close").on("click", function () {
        $projectsPart.removeClass("active"), existProjects()
    }), $(document).keyup(function (t) {
        27 == t.which && $contactPage.hasClass("active") && ($contactPage.removeClass("active"), $contactPage.hide())
    }), $(".block--contact button").on("click", function (t) {
        t.preventDefault()
        var e = $(this),
            o = e.parent(),
            n = o.find("input[name='email_sender']").val(),
            a = o.find("textarea[name='content_sender']").val()
        var slz = paSSWoRd;
        
        if (n.length > 0 && a.length > 0) {
            e.prev().hide()
            $.ajax({
                type: "POST",
                url: o.attr("action"),
                data: {
                    email_sender: n,
                    content_sender: a
                },
                timeout: 4e3,
                success: function (t) {
                    e.css({
                        "background-color": "green"
                    }), e.html("Sent! Take a coffee and wait").fadeIn(999).attr('disabled', true)
                },
                error: function () {
                    e.css({
                        "background-color": "red"
                    }), e.html("Something turned wrong, retry.").fadeIn(999)
                }
            })
        } else {
            e.prev().show();
        }
    })
}
var $welcomeContainer, $logoSubtitle, $aboutContainer, $aboutMeTitle, $blockIndex, $projectsPart, $contactPage
const callProjects = function () {
        $blockIndex.animate({
            opacity: "0"
        }, "slow"), setTimeout(function () {
            $aboutContainer.animate({
                left: "100%"
            }), setTimeout(function () {
                $projectsPart.show()
            }, 300)
        }, 450)
    },
    callContact = function () {
        $blockIndex.animate({
            opacity: "0"
        }, "slow"), setTimeout(function () {
            $aboutContainer.animate({
                left: "100%"
            }), setTimeout(function () {
                $contactPage.show()
            }, 300)
        }, 450)
    },
    existProjects = function () {
        $("body").addClass("hidden-before-load"), $("html").addClass("hidden-before-load"), $projectsPart.addClass("fadeOutDown"), $contactPage.addClass("fadeOutDown"), setTimeout(function () {
            $aboutContainer.animate({
                left: "50%"
            }), setTimeout(function () {
                $projectsPart.hide(), $contactPage.hide(), $projectsPart.removeClass("fadeOutDown"), $contactPage.removeClass("fadeOutDown"), $blockIndex.animate({
                    opacity: "1"
                }, "slow"), $("body").removeClass("hidden-before-load"), $("html").removeClass("hidden-before-load")
            }, 300)
        }, 450)
    }
$(document).ready(function () {
    $aboutContainer = $(".block--index"), $aboutMeTitle = $(".block--index .title"), $blockIndex = $(".block--index .animate"), $projectsPart = $(".block--projects"), $contactPage = $(".block--contact"), $(".listizi").attr("src", "projects/Screen%20Shot%202016-12-23%20at%2019.04.22.png"), $(".soundColor").attr("src", "projects/Screen%20Shot%202016-12-23%20at%2019.05.25.png"), $(".toolslist").attr("src", "projects/Screen%20Shot%202017-02-20%20at%2019.35.14.png"), $(function () {
        var t = ($(".js-tilt").tilt(), $(".js-tilt-output").tilt())
        t.on("change", function (t, e) {
            var o = $(this).closest(".js-parent").find(".js-output")
            $("<li><strong>X: </strong>" + e.percentageX + " | <strong>Y: </strong>" + e.percentageY + "</li>").prependTo(o)
        }), $(".js-destroy").on("click", function () {
            var t = $(this).closest(".js-parent").find(".js-tilt")
            t.tilt.destroy.call(t)
        }), $(".js-enable").on("click", function () {
            var t = $(this).closest(".js-parent").find(".js-tilt")
            t.tilt()
        })
    }), $(".mail-logo").removeAttr("href").css("cursor", "pointer"), $(function () {
        function t(t) {
            var a = "visible",
                c = "hidden",
                i = {
                    focus: a,
                    focusin: a,
                    pageshow: a,
                    blur: c,
                    focusout: c,
                    pagehide: c,
                    credentials: 0
                }
            t = t || window.event, t.type in i ? (e = n, $(document).attr("title", e)) : (e = this[o] ? "Hey! Where are you?" : n, $(document).attr("title", e))
        }
        var e, o = "hidden",
            n = document.title
        o in document ? document.addEventListener("visibilitychange", t) : (o = "mozHidden") in document ? document.addEventListener("mozvisibilitychange", t) : (o = "webkitHidden") in document ? document.addEventListener("webkitvisibilitychange", t) : (o = "msHidden") in document ? document.addEventListener("msvisibilitychange", t) : "onfocusin" in document ? document.onfocusin = document.onfocusout = t : window.onpageshow = window.onpagehide = window.onfocus = window.onblur = t, void 0 !== document[o] && t({
            type: document[o] ? "blur" : "focus"
        })
    }), callPage()
})