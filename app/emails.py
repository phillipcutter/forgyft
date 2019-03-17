from django.core.mail import send_mail

from django.conf import settings
settings.ANYMAIL["SENDGRID_API_KEY"] = "***REMOVED***"

recipients = [
    "mrfleap@gmail.com", 
    "sanu.sohum@gmail.com"
    "onekinkstar@gmail.com",
    "maconlisha@gmail.com",
    "Knatashamilliken@gmail.com",
    "nanugen19@gmail.com",
    "Moos2me@yahoo.com ",
    "mirandarider15@gmail.com",
    "Tanisha054jones@gmail.com",
    "melmanlee@hotmail.com",
    "ilove2rt@aol.com",
    "Mandinka79@aol.com",
    "renovickx@gmail.com",
    "kevinlvsravens@yahoo.com",
    "ggmagence02@gmail.com",
    "tryoung1@yahoo.com",
    "LeeKDyer@gmail.com",
    "mylildiva239@gmail.com",
    "Brenda.straka@yahoo.com",
    "angelahogan2007@gmail.com",
    "grammy513712@gmail.com ",
    "kschon06@yahoo.com",
    "Cstanfld79@gmail.com",
    "Kral.gabby@gmail.com",
    "Nancy.lewter@gmail.com",
    "cristina.sanmartin@outlook.com",
    "jessicaonken18@gmail.com",
    "dwilson2999@yahoo.com",
    "Pinkgirlicious776@aol.com",
    "pixydust0529@gmail.com",
    "RachelleWesterman@hotmail.com",
    "tiffanylovespurple19@gmail.com",
    "gvikash293@gmail.com",
    "Louanngholden@gmail.com",
    "Leaharthur4@gmail.com",
    "photog.anna@gmail.com",
    "sweetxpepper@yahoo.com",
    "beckybrit1985@gmail.com",
    "phoebesnider5768@Gmail.com",
    "Kaylamalley24@yahoo.com",
    "benandcrissy@gmail.com",
    "kendall1987.ka@gmail.com",
    "saundersannem@gmail.com",
    "lgodbout23@gmail.com",
    "sonicharris456@gmail.com",
    "lewislea21@gmail.com",
    "thaze@nrgmedia.com",
    "Amyket@yahoo.com",
    "Samantha.Annarino1031@gmail.com",
    "Imtoocoolforspam@gmail.com",
    "ekrietz@earthlink.net",
    "Twistedhippy7@gmail.com",
    "02mom1216@gmail.com",
    "escatellol92@gmail.com",
    "Ohkayso20@gmail.com",
    "Detroitsteed@gmail.com ",
    "m.j171@yahoo.com",
    "yahyaabdikadir2000@gmail.com",
    "energyrohan@gmail.com",
    "adityarao@gmail.com"
    ]

# recipients = [
#     "mrfleap@gmail.com", 
#     "sanu.sohum@gmail.com"
# ]

for recipient in recipients:

    send_mail(
        'Forgift Expert Program Opportunity',
    """
    Hi!

    Thanks for expressing interest in Forgift’s Expert Program!

    We are currently looking for gift “experts” or individuals who are creative and
    love giving gift recommendations as a hobby. Additionally, if you have
    knowledge about one particular interest such as: Sports, Art, Animals, Video
    Games, Music, Makeup, Clothes, Reading, and Movies; we would love to work
    with you!

    So, what do experts do?

    An expert is someone who helps fulfill gift requests for Forgift! A gift request consists of the gift receiver’s age, gender, occasion, and interests along with the gift givers budget and relationship to the gift receiver. We love creativity so everything unique and outside the box is perfect! To become an expert, all you have to do is go to www.forgift.org/experts, signup, and fill out an example gift request. It as easy as that!
    Reply to this email if you have any comments or questions!

    Thanks – The Forgift Team
    """,
        'support@forgift.org',
        [recipient],
        fail_silently=False,
        html_message="""
    <p>
    Hi!

    Thanks for expressing interest in Forgift’s Expert Program!<br><br>

    We are currently looking for gift “experts” or individuals who are creative and
    love giving gift recommendations as a hobby. Additionally, if you have
    knowledge about one particular interest such as: Sports, Art, Animals, Video
    Games, Music, Makeup, Clothes, Reading, and Movies; we would love to work
    with you!<br><br>

    So, what do experts do?<br><br>

    An expert is someone who helps fulfill gift requests for Forgift! A gift request consists of the gift receiver’s age, gender, occasion, and interests along with the gift givers budget and relationship to the gift receiver. We love creativity so everything unique and outside the box is perfect! To become an expert, all you have to do is go to www.forgift.org/experts, signup, and fill out an example gift request. It as easy as that!
    Reply to this email if you have any comments or questions!<br><br>

    Thanks – The Forgift Team
    </p>
    """
    )
