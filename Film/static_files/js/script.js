$(function() {
    $("#lbBox img").hide();
    $(".bodySpreadBox img").hide();
    $("#lbBox img:first").show();
    $(".bodySpreadBox img:first").show();
    $(".point").eq(0).addClass("pointOn");

    var dotIndex = 0;
    $(".point").click(function () {
        dotIndex = $(this).index();
        $("#lbBox>img").eq(dotIndex).show().siblings().hide();
        $(".bodySpreadBox img").eq(dotIndex).show().siblings().hide();
        $(this).addClass("pointOn").siblings().removeClass("pointOn");
    });
    $('.lbLeftButton').click(function () {
        dotIndex = dotIndex - 1;
        $("#lbBox>img").eq(dotIndex).show().siblings().hide();
        $(".bodySpreadBox img").eq(dotIndex).show().siblings().hide();
        $(".point").eq(dotIndex).addClass("pointOn").siblings().removeClass("pointOn");
    });
    $('.lbRightButton').click(function () {
        dotIndex = dotIndex + 1;
        $("#lbBox>img").eq(dotIndex).show().siblings().hide();
        $(".bodySpreadBox img").eq(dotIndex).show().siblings().hide();
        $(".point").eq(dotIndex).addClass("pointOn").siblings().removeClass("pointOn");
    });

    //轮播
    function play() {
        dotIndex = (dotIndex + 1) % 4;
        $("#lbBox>img").eq(dotIndex).show().siblings().hide();
        $(".bodySpreadBox img").eq(dotIndex).show().siblings().hide();
        $(".point").eq(dotIndex).addClass("pointOn").siblings().removeClass("pointOn");
    }

    var autoPlay = setInterval(play, 2000);

    $("#lbBox>img").hover(function () {
        clearInterval(autoPlay);
    }, function () {
        autoPlay = setInterval(play, 2000);
    });
    $('.lbLeftButton').hover(function () {
        clearInterval(autoPlay);
    }, function () {
        autoPlay = setInterval(play, 2000);
    });
    $('.lbRightButton').hover(function () {
        clearInterval(autoPlay);
    }, function () {
        autoPlay = setInterval(play, 2000);
    });
    $(".bodySpreadBox img").hover(function () {
        clearInterval(autoPlay);
    }, function () {
        autoPlay = setInterval(play, 2000);
    });

    //searchButton
    $(".headerSearchLineBoxButton").hover(function () {
        $(this).addClass("buttonOn");
    }, function () {
        $(this).removeClass("buttonOn");
    });

    //More
    $(".More").hover(function () {
        $(this).addClass("moreOn");
    }, function () {
        $(this).removeClass("moreOn");
    });

    //click then playbox show
    $(".bodyContentBox").click(function () {
        $(".playBox").addClass('playBoxAnimationDown');
        $(".playBox").removeClass('playBoxAnimationUp');
    });

    $(".bottomButtonBox").click(function () {
        $(".playBox").addClass('playBoxAnimationUp');
        $(".playBox").removeClass('playBoxAnimationDown');
    });

    $(".loginButton").click(function () {
        $(".cover").css("display", "block");
        $(".login_block").css("display", "block");
        //为了不让登录框显示的时候，仍然能滚动页面
        $("body").css("overflow", "hidden")
    });

    $(".registerButton").click(function () {
        $(".cover").css("display", "block");
        $(".register_block").css("display", "block");
        //为了不让登录框显示的时候，仍然能滚动页面
        $("body").css("overflow", "hidden")
    });

    $('.register_now').click(function () {
        $(".login_block").css("display", "none");
        $(".register_block").css("display", "block");
    });

    $(".closeButton").click(function () {
        $(".cover").css("display", "none");
        $(".register_block").css("display", "none");
        $(".login_block").css("display", "none");
        $("body").css("overflow", "visible");
    });

    //查看更多
    var clickCount = 0;
    $(".More").click(function () {
        clickCount += 1;
        newLineHeight = 1000 + 960 * clickCount;
        newBodyerHeight = 1250 + 960 * clickCount;
        $(".bodyContentLine").css('height', newLineHeight.toString() + 'px');
        $(".bodyer").css('height', newBodyerHeight.toString() + 'px');
    });

    var name;
    $(".bodyContentBox").click(function () {
        var index = $(".bodyContentBox").index(this);
        welcome = $('.welcome').html();
        if (welcome == undefined) {
            name = $(".bodyContentBox").eq(index).find("b").text();
            $.get("/getInfo_nlogin", {'name': name}, function (ret) {
                $(".playBox").html(ret);
            })
        } else {
            name = $(".bodyContentBox").eq(index).find("b").text();
            $.get("/getInfo", {'name': name}, function (ret) {
                $(".playBox").html(ret);
            })
        }
    });

    var audioIndex;
    audioIndex = 0;
    var s0 = new Audio('/static/久石让-シータとパズー(《天空之城》动漫插曲).mp3');
    $('.cd').click(function () {
        if (audioIndex % 2) {
            $('.arm').css('animation', 'armDown_animation 1s forwards');
            $('.cd').css('animation', '');
            $('.runLine').css('animation-play-state', 'paused');
            audioIndex += 1;
            s0.pause();
        } else {
            $('.arm').css('animation', 'armRaise_animation 1s forwards');
            $('.cd').css('animation', 'cd_animation 2s linear infinite');
            $('.runLine').css('background', '#a8b10a');
            $('.runLine').css('animation', 'runLineAnimation 279s linear forwards');
            audioIndex += 1;
            s0.play();
        }
    });

    $(".bodyFirstLine li").eq(0).css('color', '#1e7dd7');
    var typeIndex;
    $('.bodyFirstLine li').click(function () {
        typeIndex = $(".bodyFirstLine li").index(this);
        type = $(".bodyFirstLine li").eq(typeIndex).text();
        $(".bodyFirstLine li").eq(typeIndex).children('a').css('color', '#1e7dd7');
        $(".bodyFirstLine li").eq(typeIndex).sibling('li').children('a').css('color', 'gray');
    });

    //注册校验
    $('.userNameInput').bind('input propertychange change', function () {
        var username = $(this).val();
        if (username == '') {
            $('.register_success').html('');
            $('.register_failure').html('用户名不能为空')
        } else {
            $.get('/verify/', {'username': username}, function (ret) {
                if (ret == '用户名已存在') {
                    $('.register_success').html('');
                    $('.register_failure').html('用户名已存在');
                } else {
                    $('.register_failure').html('');
                    $('.register_success').html('用户名可用');
                }
            })
        }
    });

    $('.passWordInput').bind('input propertychange change', function () {
        var password = $('.passWordInput').val();
        var r_password = $('.r_passWordInput').val();
        if (password == '') {
            $('.register_success').html('');
            $('.register_failure').html('密码不能为空');
        } else if (password == r_password) {
            $('.register_success').html('校验通过');
            $('.register_failure').html('');
        } else if (password != r_password && r_password != '') {
            $('.register_success').html('');
            $('.register_failure').html('两次密码输入不一致');
        } else {
            $('.register_success').html('');
            $('.register_failure').html('');
        }
    });

    $('.r_passWordInput').bind('input propertychange change', function () {
        var password = $('.passWordInput').val();
        var r_password = $('.r_passWordInput').val();
        if (password == '') {
            $('.register_failure').html('请输入密码');
            $('.register_success').html('');
        } else if (password == r_password) {
            $('.register_success').html('校验通过');
            $('.register_failure').html('');
        } else if (password != r_password) {
            $('.register_failure').html('两次密码输入不一致');
            $('.register_success').html('');
        } else {
            $('.register_success').html('');
            $('.register_failure').html('');
        }
    });

    $('.myCollectButton').click(function () {
        $('.myCollectBox').css('display', 'block');
        $.get('/getMyCollection', {}, function (ret) {
            $('.mcContentBox').html(ret);
        });
    });

    $('.close_myCollection').click(function () {
        $('.myCollectBox').css('display', 'none');
    });

    var commentIndex = 0;
    $('.comment_animation_button').click(function () {
        if (commentIndex % 2) {
            $('.write_comment_box').css('animation', 'comment_down_animation 1s forwards');
            commentIndex += 1;
        } else {
            $('.write_comment_box').css('animation', 'comment_up_animation 1s forwards');
            commentIndex += 1;
        }
    });

    $('.closeComment').click(function () {
        $('.myCommentBox').css('display', 'none');
        $('.write_comment_box').css('display', 'none');
    });

    $('.send_comment_button').click(function () {
        var comment_text = $('.comment_write_Text').val();
        var film_name = $('.infos_name').text();
        $.get('/write_comment', {'comment_text': comment_text, 'film_name': film_name}, function (ret) {
            $('.commentBox').html(ret);
        })
    });

    //弹幕
    function randNum(minnum, maxnum) {
        return Math.floor(minnum + Math.random() * (maxnum - minnum));
    }

    var c = 0;

    function myFunction() {
        setInterval(function () {
            c += 1;
            $.get('/get_barrage', {'now_count': c}, function (ret) {

                $('.rollBarrageBox').append(ret);
            });
        }, 1000);
    }
    clearInterval();
    $('.playButton').click(myFunction());

    var boxHeight = $('.rollBarrageBox').height();
    $('.writeBarrageButton').click(function () {
        var barrage_text = $('.writeBarrageInput').val();
        var film_name = $('.infos_name').text();

        var rand_height = parseInt(Math.random() * (boxHeight / 1) - 30);
        var rand_color = randNum(100000, 999999);
        var rand_fontsize = randNum(18, 25);
        var rand_id = parseInt(Math.random() * 999999);

        $('<span style="animation: spanAnimation 14s linear forwards;"></span>').appendTo('.rollBarrageBox');
        $('.rollBarrageBox span:last').css('id', rand_id);
        $('.rollBarrageBox span:last').css('top', rand_height+'px');
        $('.rollBarrageBox span:last').css('color', '#' + rand_color);
        $('.rollBarrageBox span:last').css('font-size', rand_fontsize + 'px');
        $('.rollBarrageBox span:last').html(barrage_text);

        $.get('/send_barrage', {'timeCount': c, 'barrageText': barrage_text, 'film_name': film_name});
    });

    $(function() {
            setInterval(function () {
                $('.circle').remove();
            }, 5000);
        });

});