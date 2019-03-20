function callPage() {
    setTimeout(function () {
        $aboutContainer.animate({
            left: "50%",
            width: "50%"
        }), $aboutMeTitle.show(), $blockIndex.show(), $("body").removeClass("hidden-before-load"), $("html").removeClass("hidden-before-load")
    }, 300), $(".mail-logo").on("click", function () {
        callContact(), $contactPage.addClass("active") // pass
    }), $(".block--contact .close").on("click", function () {
        $contactPage.removeClass("active"), existProjects()
    }), $(document).keyup(function (t) {
        27 == t.which && $contactPage.hasClass("active") && ($contactPage.removeClass("active"), $contactPage.hide())
    }), $(".block--contact button").on("click", function (t) {
        t.preventDefault()
        var e = $(this),
            o = e.parent(),
            key = "kzdKOSZOQdz4dq5zqd745",
            n = o.find("input[name='email_sender']").val(),
            a = o.find("textarea[name='content_sender']").val()
        
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
   