from django.core.mail import send_mail

from django.conf import settings
settings.ANYMAIL["SENDGRID_API_KEY"] = "***REMOVED***"
settings.EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"

# $("#emails").children().each(function() {
#    email = $(this).children().first().text()
#    console.log('"' + email + '",')
# });+

# recipients = [
#     # "vzollman57@gmail.com ",
#     # "purplepup26@gmail.com",
#     # "cochese1992@msn.com",
#     # "Jessicaandkevin@mail.com",
#     # "millercarolyn909@gmail.com",
#     # "mstockeland54@gmail.com",
#     # "Esmejazz3@gmail.com ",
#     # "Dianaborn58@gmail.com",
#     # "altondillon@hotmail.com ",
#     # "0@no.you",
#     # "Cali50462@gmail.com ",
#     # "Erin.elizabeth.mail@yahoo.com",
#     # "Acfilters@gcecisp.com",
#     # "hdannenbring @mac.com",
#     # "angehester@yahoo.com",
#     # "dr.cindybigsby@gmail.com",
#     # "turbowitch1@yahoo.com",
#     # "onekinkstar@gmail.com",
#     # "maconlisha@gmail.com",
#     # "Knatashamilliken@gmail.com",
#     # "nanugen19@gmail.com",
#     # "melmanlee@hotmail.com",
#     # "Mandinka79@aol.com",
#     # "renovickx@gmail.com",
#     # "kevinlvsravens@yahoo.com",
#     # "ggmagence02@gmail.com",
#     # "LeeKDyer@gmail.com",
#     # "mylildiva239@gmail.com",
#     # "angelahogan2007@gmail.com",
#     # "grammy513712@gmail.com ",
#     # "Cstanfld79@gmail.com",
#     # "Kral.gabby@gmail.com",
#     # "Nancy.lewter@gmail.com",
#     # "cristina.sanmartin@outlook.com",
#     # "jessicaonken18@gmail.com",
#     # "Pinkgirlicious776@aol.com",
#     # "RachelleWesterman@hotmail.com",
#     "tiffanylovespurple19@gmail.com",
#     "gvikash293@gmail.com",
#     "Louanngholden@gmail.com",
#     "Leaharthur4@gmail.com",
#     "photog.anna@gmail.com",
#     "sweetxpepper@yahoo.com",
#     "beckybrit1985@gmail.com",
#     "phoebesnider5768@Gmail.com",
#     "Kaylamalley24@yahoo.com",
#     "kendall1987.ka@gmail.com",
#     "lgodbout23@gmail.com",
#     "sonicharris456@gmail.com",
#     "lewislea21@gmail.com",
#     "thaze@nrgmedia.com",
#     "Amyket@yahoo.com",
#     "Samantha.Annarino1031@gmail.com",
#     "Imtoocoolforspam@gmail.com",
#     "ekrietz@earthlink.net",
#     "02mom1216@gmail.com",
#     "escatellol92@gmail.com",
#     "m.j171@yahoo.com",
#     "mrfleap@gmail.com",
#     "sanu.sohum@gmail.com"
# ]

# users = User.objects.all()
# for user in users:
#     if user.email.lower().strip() in [email.lower().strip() for email in recipients]:
#         recipients.pop([email.lower().strip() for email in recipients].index(user.email.lower().strip()))
#
# for recipient in recipients:
#     print('"' + recipient + '",')

# recipients = [
#     "mrfleap@gmail.com",
#     # "sanu.sohum@gmail.com"
# ]

recipients = """awesomekdi205@gmail.com
dwilson2999@yahoo.com
benandcrissy@gmail.com
moos2me@yahoo.com
ilove2rt@aol.com
cristina.sanmartin@outlook.com
yahyaabdikadir2000@gmail.com
mrfleap@gmail.com
s.sohum8@gmail.com
tanisha054jones@gmail.com
saundersannem@gmail.com""".split("\n")

# recipients = ["mrfleap@gmail.com", "sanu.sohum@gmail.com"]

expert_message = """Hi!
Forgift is following up on its expert program.

We are currently looking for gift “experts” or people who are creative and love giving gift recommendations as a hobby.

What Experts do:

An expert is someone who helps fulfill gift requests for Forgift! A gift request
will consist of the persons
Age, Gender, Relationship, Occasion, Price,
Interests, Items they own, extra information, and the receiver’s name. We
love creativity so everything unique and outside the box is perfect!
To get started, all you have to do is go to
www.forgift.org/experts
, signup,
and fill out an example gift request and voila you’re an expert!

Reply to this email if you have any comments or questions!
Thanks – The Forgift Team"""

expert_html_message = """<p>Hi!<br>
Forgift is following up on its expert program.<br><br>

We are currently looking for gift “experts” or people who are creative and love giving gift recommendations as a hobby.<br><br>

What Experts do:<br><br>

An expert is someone who helps fulfill gift requests for Forgift! A gift request
will consist of the persons
Age, Gender, Relationship, Occasion, Price,
Interests, Items they own, extra information, and the receiver’s name. We
love creativity so everything unique and outside the box is perfect!
To get started, all you have to do is go to
www.forgift.org/experts
, signup,
and fill out an example gift request and voila you’re an expert!<br><br>

Reply to this email if you have any comments or questions!<br>
Thanks – The Forgift Team
</p>"""

return_message = """Hi!
Thanks for signing up for Forgifts expert program.

We noticed that you haven't yet filled out the example gift request. When you can, please finish signing up so you 
can start fulfilling gift requests!

Finish singing up here: https://www.forgift.org/expert_profile

Please reply to this email if you have any questions.

Thanks - Forgift Team"""

return_html_message = """<p>Hi!<br>
Thanks for signing up for Forgifts expert program.<br>
<br>
We noticed that you haven't yet filled out the example gift request. When you can, please finish signing up so you 
can start fulfilling gift requests!<br>
<br>
Finish singing up here: https://www.forgift.org/expert_profile<br>
<br>
Please reply to this email if you have any questions.<br>
<br>
Thanks - Forgift Team</p>"""

for recipient in recipients:
    send_mail(
        'Follow-up on Forgift\'s Expert Program',
        return_message,
    "Forgift <support@forgift.org>",
    [recipient],
    fail_silently=False,
    )
    print("Sent email to " + str(recipient))