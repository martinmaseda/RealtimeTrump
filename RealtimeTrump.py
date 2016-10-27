# -*- coding: utf-8 -*-
import datetime
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import json
import pymongo
import tweepy
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import *
import pickle


## YOUR CREDENTIALS COME HERE
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

hashtags = ['#donaldtrump', '#trump', '#makeamericagreatagain', '#trump2016', '#americafirst', '#maga', '#tcot', '#trumptrain', '#votetrump2016',  '#republicans', '#realdonaldtrump', '#crookedhilary', '#moretrustedthanhillary', '#ccot', '#neverhilary']
users_registered_to_service = [["Christina", "christinastat@student.ie.edu", ['HarryWalker220', 'StreetrunnerGee', 'HarryWalker220', 'idktony530', 'rainbowcatband', 'Kush_aagr', 'aghayev_rafig', 'DavinaMorgan6', 'edag15', 'haiiro1100', 'BRODG24', 'duguran_nicole', 'jeremiah11703', 'estgreenspirit', 'RoryFleming8A', 'GeoffreyKisur', 'YahBoyTomBrady', 'jackjj06', 'manpreeeett_', 'DRE13WLA']],
                               ["Monica","monica.ramirez@student.ie.edu", ['phidesigner', 'Joshmauer13', 'treyg1222', 'JesseSaucedo2', 'FinnishAtTheRim', 'FinnishAtTheRim', 'mahiudd96645498', 'maltdog101', 'LynnQueen05', 'cape_rosa', 'Famsisterspirit', 'burakdemirer_', 'ThaiHaremPants', 'AaronTare', 'EllaYabsley', 'johnboybeats', 'ElObservanteMty', 'frankfafsa', 'abhijeetanpat', 'AnNikeshk762', 'ViniciusSantos']]]


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


f = open('my_tweet_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

def send_email_to(the_user,the_tweet,the_author,the_address,the_tweet_id):

    # me == my email address
    # you == recipient's email address
    fromaddr = "savingamericaorg@gmail.com"
    toaddr = the_address


    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Your friend is supporting Trump!"

    # Create the body of the message (a plain-text and an HTML version).
    #text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    html = """\
    <html xmlns="http://www.w3.org/1999/xhtml">    <head>	    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">        <meta name="viewport" content="width=device-width, initial-scale=1.0">    	<title>square gallery | Newsletter</title>        <style type="text/css">			/*////// RESET STYLES //////*/			body, #bodyTable, #bodyCell{height:100% !important; margin:0; padding:0; width:100% !important;}			table{border-collapse:collapse;}			img, a img{border:0; outline:none; text-decoration:none;}			h1, h2, h3, h4, h5, h6{margin:0; padding:0;}			p{margin: 1em 0;}			/*////// CLIENT-SPECIFIC STYLES //////*/			.ReadMsgBody{width:100%;} .ExternalClass{width:100%;} /* Force Hotmail/Outlook.com to display emails at full width. */			.ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div{line-height:100%;} /* Force Hotmail/Outlook.com to display line heights normally. */			table, td{mso-table-lspace:0pt; mso-table-rspace:0pt;} /* Remove spacing between tables in Outlook 2007 and up. */			#outlook a{padding:0;} /* Force Outlook 2007 and up to provide a "view in browser" message. */			img{-ms-interpolation-mode: bicubic;} /* Force IE to smoothly render resized images. */			body, table, td, p, a, li, blockquote{-ms-text-size-adjust:100%; -webkit-text-size-adjust:100%;} /* Prevent Windows- and Webkit-based mobile platforms from changing declared text sizes. */			/*////// MOBILE STYLES //////*/			@media only screen and (max-width: 480px){				/*////// RESET STYLES //////*/				td[id="introductionContainer"], td[id="callToActionContainer"], td[id="eventContainer"], td[id="merchandiseContainer"], td[id="footerContainer"]{padding-right:10px !important; padding-left:10px !important;}				table[id="introductionBlock"], table[id="callToActionBlock"], table[id="eventBlock"], table[id="merchandiseBlock"], table[id="footerBlock"]{max-width:480px !important; width:100% !important;}								/*////// CLIENT-SPECIFIC STYLES //////*/				body{width:100% !important; min-width:100% !important;} /* Force iOS Mail to render the email at full width. */								/*////// GENERAL STYLES //////*/				h1{font-size:34px !important;}				h2{font-size:30px !important;}				h3{font-size:24px !important;}								img[id="heroImage"]{height:auto !important; max-width:1200px !important; width:100% !important;}								td[class="introductionLogo"], td[class="introductionHeading"]{display:block !important;}				td[class="introductionHeading"]{padding:40px 0 0 0 !important;}				td[class="introductionContent"]{padding-top:20px !important;}								td[class="callToActionContent"]{text-align:left !important;}				table[class="callToActionButton"]{width:100% !important;}								td[id="eventBlockCell"]{padding-right:20px !important; padding-left:20px !important;}				table[class="eventBlockCalendar"]{width:100px !important;}								td[id="merchandiseBlockCell"]{padding-right:20px !important; padding-left:20px !important;}				td[class="merchandiseBlockHeading"] h2{text-align:center !important;}				td[class="merchandiseBlockLeftColumn"], td[class="merchandiseBlockRightColumn"]{display:block !important; padding:0 0 20px 0 !important; width:100% !important;}				td[class="footerContent"]{font-size:15px !important;}				td[class="footerContent"] a{display:block;}			}		</style>    </head>    <body style="margin: 0;padding: 0;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #424145;height: 100%;width: 100%;">    	<center>        	<table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;margin: 0;padding: 0;background-color: #424145;height: 100%;width: 100%;">            	<tr>                	<td align="center" valign="top" id="bodyCell" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;margin: 0;padding: 0;height: 100%;width: 100%;">                    	<!-- // BEGIN EMAIL -->                        <table border="0" cellpadding="0" cellspacing="0" width="100%" id="emailContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;width: 100%;">                        	<tr>                            	<td align="center" valign="top" id="heroImageContainer" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #F0F0F0;">                                    <!-- // BEGIN HERO BLOCK -->                                    <img src="https://s3-us-west-2.amazonaws.com/martinmaseda/WhatsApp-Image-20160707.jpeg" alt="In The Conservatory, by Édouard Manet" height="415" width="1200" id="heroImage" style="border: 0;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;">                                    <!-- END HERO BLOCK // -->                                </td>                            </tr>                        	<tr>                            	<td align="center" valign="top" id="introductionContainer" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #F0F0F0;padding: 40px;">                                    <!-- // BEGIN INTRO BLOCK -->                                    <table border="0" cellpadding="0" cellspacing="0" width="520" id="introductionBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #F0F0F0;">                                        <tr>                                            <td style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">                                                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">                                                    <tr>                                                        <td align="center" valign="top" class="introductionLogo" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">                                                                                                                 </td>                                                        <td align="middle" valign="middle" class="introductionHeading" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;color: #808080;font-size: 14px;font-weight: bold;line-height: 150%;padding-left: 40px;">                                                                                                                        <br>                                                            <h1 style="margin: 0;padding: 0;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;color: #D83826;font-size: 45px;font-weight: 100;line-height: 115%;text-align: middle;">{the_user}, your friend {the_author} just tweeted in favour of Donald Trump!! </h1>                                                        </td>                                                    </tr>                                                </table>                                            </td>                                        </tr>                                        <tr>                                            <td align="left" valign="top" class="introductionContent" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;color: #606060;font-size: 18px;line-height: 150%;padding-top: 40px;">                                                We know, we couldn't believe it ourselves either... However, you can help your friends coming to their senses by replying to this tweet NOW!!                                              </td>                                        </tr>                                    </table>                                    <!-- END INTRO BLOCK // -->                                </td>                            </tr>                        	<tr>                            	<td align="center" valign="top" id="callToActionContainer" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #D83826;padding: 40px;">                                    <!-- // BEGIN CALL-TO-ACTION BLOCK -->                                    <table border="0" cellpadding="0" cellspacing="0" width="520" id="callToActionBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #D83826;">                                        <tr>                                            <td align="center" valign="top" class="callToActionContent" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;color: #FFFFFF;font-size: 16px;line-height: 150%;padding-bottom: 40px;text-align: center;">                                                <h3 style="margin: 0;padding: 0;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;color: #FFFFFF;font-size: 30px;font-weight: 100;line-height: 115%;text-align: center;">{the_tweet}<br>Click below to reply to your friend {the_author}</h3>                                                <br>                                                                                            </td>                                        </tr>                                        <tr>                                            <td align="center" valign="top" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">                                                <table border="0" cellpadding="0" cellspacing="0" class="callToActionButton" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #F0F0F0;border-radius: 4px;box-shadow: 0 5px 0 #A22A1C;">                                                    <tr>                                                        <td align="center" valign="top" class="callToActionButtonContent" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;padding-top: 20px;padding-right: 40px;padding-bottom: 20px;padding-left: 40px;color: #D83826;display: block;font-size: 24px;font-weight: bold;line-height: 100%;letter-spacing: -1px;text-align: center;text-decoration: none;">                                                            <a href="https://twitter.com/groupa/status/{the_tweet_id}" target="_blank" title="square gallery" style="-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #D83826;display: block;font-size: 24px;font-weight: bold;line-height: 100%;letter-spacing: -1px;text-align: center;text-decoration: none;">Reply Now</a>                                                        </td>                                                    </tr>                                                </table>                                            </td>                                        </tr>                                    </table>                                    <!-- //END CALL-TO-ACTION BLOCK -->                                </td>                            </tr>                        	<tr>                            	<td align="center" valign="top" id="eventContainer" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #F0F0F0;padding: 40px;">                                    <!-- // BEGIN EVENT BLOCK -->                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="eventBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #F0F0F0;border-top: 1px solid #BBBBBB;border-bottom: 1px solid #BBBBBB;">                                        <tr>                                            <td align="center" valign="top" id="eventBlockCell" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;padding: 40px;">                                                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">                                                    <tr>                                                        <td align="left" valign="top" class="eventBlockHeading" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;padding-bottom: 40px;">                                                            <h2 style="margin: 0;padding: 0;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;color: #606060;font-size: 34px;font-weight: 100;line-height: 100%;text-align: left;">Upcoming Events</h2>                                                        </td>                                                    </tr>                                                    <tr>                                                        <td align="center" valign="top" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">                                                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">                                                                <tr>                                                                    <td align="center" valign="top" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">                                                                        <table border="0" cellpadding="0" cellspacing="0" width="110" class="eventBlockCalendar" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border: 1px solid #DDDDDD;">                                                                            <tr>                                                                                <td align="center" valign="top" class="eventBlockMonth" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;background-color: #D83826;color: #FFFFFF;font-size: 18px;font-weight: bold;line-height: 100%;padding: 10px;">                                                                                    OCT                                                                                </td>                                                                            </tr>                                                                            <tr>                                                                                <td align="center" valign="top" class="eventBlockDay" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;background-color: #FFFFFF;color: #404040;font-size: 48px;font-weight: bold;line-height: 100%;padding: 15px;">                                                                                    21                                                                                </td>                                                                            </tr>                                                                        </table>                                                                    </td>                                                                    <td align="left" valign="top" class="eventContent" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;color: #606060;font-size: 16px;line-height: 125%;padding-left: 20px;">                                                                        <h3 style="margin: 0;padding: 0;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;color: #D83826;font-size: 30px;font-weight: 100;line-height: 115%;text-align: left;">Dump Trump</h3>                                                                        <strong>Why Donald Trump when you can dump Donald? October 27</strong>                                                                        <br>                                                                        1001 reasons about the negative impact Donald's presidency will have in your children's future (and those of the rest of the free world)                                                                    </td>                                                                </tr>                                                            </table>                                                        </td>                                                    </tr>                                                </table>                                            </td>                                        </tr>                                    </table>                                    <!-- END EVENT BLOCK // -->                                    <!-- // BEGIN FOOTER BLOCK -->                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="footerBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">                                        <tr>                                            <td align="center" valign="top" class="footerContent" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;color: #AAAAAA;font-size: 13px;line-height: 150%;padding-bottom: 40px;">                                                <strong>Thank you for helping the world to take the Donald down </strong>                                            </td>                                        </tr>                                        <tr>                                            <td align="center" valign="top" class="footerContent" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;color: #AAAAAA;font-size: 13px;line-height: 150%;padding-bottom: 40px;">                                                &copy; 2016 Group A. &bull; IE Business School &bull; Master in Business Analytics and Big Data                                                <br>                                                <br>                                                <a href="#" target="_blank" style="-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #D83826;text-decoration: none;">unsubscribe from list</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="#" target="_blank" style="-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #D83826;text-decoration: none;">set email preferences</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="#" target="_blank" style="-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #D83826;text-decoration: none;">view in browser</a>                                            </td>                                        </tr>                                    </table>                                    <!-- END FOOTER BLOCK // -->                                </td>                            </tr>                        </table>                        <!-- END EMAIL // -->                    </td>                </tr>            </table>        </center>    </body></html>
    """
    html = html.replace("{the_user}", the_user)
    html = html.replace("{the_tweet}", the_tweet)
    html = html.replace("{the_author}", the_author)
    html = html.replace("{the_tweet_id}", the_tweet_id)


    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "GroupAMBD")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def get_words_from_sentence(list_of_tokenized_words):
    stemmer = PorterStemmer()
    list_of_tokenized_words = [cap_word.lower() for cap_word in list_of_tokenized_words]
    list_of_tokenized_words = [each_word for each_word in list_of_tokenized_words if each_word not in stopwords.words('english')]
    list_of_tokenized_words = [each_word for each_word in list_of_tokenized_words if each_word not in [",", ".", "..", "...", ":", "?", "!", "\'", "\"", "#", "-", "_", "(", ")"]]
    list_of_tokenized_words = [stemmer.stem(each_word) for each_word in list_of_tokenized_words]
    return list_of_tokenized_words


def word_feats(words):
    return dict([(word, True) for word in get_words_from_sentence(words)])


def tokenize_sentence_into_list_of_words(sentence):
    tknzr = TweetTokenizer()
    list_of_tokenized_words = tknzr.tokenize(sentence)
    return list_of_tokenized_words

def check_if_friend_did_it(list_of_friends, tweeter_owner):
    if tweeter_owner in list_of_friends:
        return True
    else:
        return False

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        self.db = pymongo.MongoClient().test
        self.db.tweets.drop()
        self.apple_counter = 0
        self.android_counter = 0
        self.happy_barcelona = 0
        self.happy_madrid = 0
        self.sad_barcelona = 0
        self.sad_madrid = 0
        self.total_madrid = 0
        self.total_barcelona = 0

    def on_data(self, tweet):
        start_time = datetime.datetime.now()
        jsontweet = json.loads(tweet)

        if "text" in jsontweet:
            if "user" in jsontweet:
                if "screen_name" in jsontweet["user"]:
                    tweet_text = jsontweet["text"]
                    owner_of_the_tweet = jsontweet["user"]["screen_name"]
                    tweet_id = jsontweet["id_str"]
                    tweet_contains_trump = False
                    tweet_must_be_targetted = False
                    users_to_notify = []

                    for trump_tag in hashtags:
                        if trump_tag in tweet_text:
                            tweet_contains_trump = True

                    if tweet_contains_trump:
                        print(jsontweet["text"])
                        if classifier.prob_classify(word_feats(tokenize_sentence_into_list_of_words(tweet_text))).max() == "pos":
                            tweet_must_be_targetted = True

                    tweet_must_be_targetted = True

                    if tweet_must_be_targetted and tweet_contains_trump:
                        users_to_notify = [(item[0], item[1]) for item in users_registered_to_service if check_if_friend_did_it(item[2], owner_of_the_tweet)]

                    for user_to_notify in users_to_notify:
                        send_email_to(user_to_notify[0], tweet_text, owner_of_the_tweet, user_to_notify[1], tweet_id)
                        time_it_took = datetime.datetime.now() - start_time
                        print("Email sent to: " + str(user_to_notify[0]) + " in " + str(time_it_took.microseconds) + " microseconds since the tweet occurred")


    def on_error(self, status_code):
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream


sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.filter(follow=None, locations=[-4.735107421875,39.842286020743394,3.109130859375,41.934976500546604])
