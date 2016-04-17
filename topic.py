
from flask import Flask
app = Flask(__name__)
import pprint
from gensim import corpora, models, similarities, matutils
import re
import pandas as pd
from operator import itemgetter

from flask import request
import json

import random



pp = pprint.PrettyPrinter()
number_topics=7
stop=[]
with open('stoplist-multilingual.txt') as f:
    stop=f.readlines()
    stop=[word.strip('\n') for word in stop]
our_texts = ["Yes!","It's so crazy right now!","Most incredibly, it's ya girl, Bee,","It's ya boy, young.","You ready?","Uh oh, uh oh, uh oh, oh no no","Uh oh, uh oh, uh oh, oh no no","Uh oh, uh oh, uh oh, oh no no","Uh oh, uh oh, uh oh, oh no no","Yea, history in the making,","Part 2, it's so crazy right now","I look and stare so deep in your eyes,","I touch on you more and more every time,","When you leave I'm begging you not to go,","Call your name two or three times in a row,","Such a funny thing for me to try to explain,","How I'm feeling and my pride is the one to blame.","'Cuz I know I don't understand,","Just how your love can do what no one else can.","Got me looking so crazy right now, your love's","Got me looking so crazy right now (in love)","Got me looking so crazy right now, your touch","Got me looking so crazy right now (your touch)","Got me hoping you'll page me right now, your kiss","Got me hoping you'll save me right now","Looking so crazy in love's,","Got me looking, got me looking so crazy in love.","Uh oh, uh oh, uh oh, oh no no","Uh oh, uh oh, uh oh, oh no no","Uh oh, uh oh, uh oh, oh no no","Uh oh, uh oh, uh oh, oh no no","When I talk to my friends so quietly,","Who he think he is? Look at what you did to me,","Tennis shoes, don't even need to buy a new dress,","If you ain't there ain't nobody else to impress,","The way that you know what I thought I knew,","It's the beat my heart skips when I'm with you,","But I still don't understand,","Just how your love can do what no one else can.","Got me looking so crazy right now, your love's","Got me looking so crazy right now (oh crazy)","Got me looking so crazy right now, your touch (you're in love)","Got me looking so crazy right now (love!)","Got me hoping you'll page me right now, your kiss (hey!)","Got me hoping you'll save me right now","Looking so crazy in love's, (hey)","Got me looking, got me looking so crazy in love.","I'm Looking so crazy in love's,","Got me looking, got me looking so crazy in love.","Check it, let's go","Young Hov y'all know when the flow is loco,","Young B and the R-O-C, uh oh, (oh)","Ol' G, big homie, the one and only,","Stick bony, but the pocket is fat like Tony, Soprano, (oh no)","The ROC handle like Van Axel,","I shake phoneys man, You can't get next to,","The genuine article I go I do not sing though,","I sling though, If anything I bling yo,","Star like Ringo, war like a green berret","Crazy bring your whole set,","Jay-Z in the range, crazy and deranged,","They can't figure them out they like hey is he insane, (oh no)","Yes sir I'm cut from a different cloth,","My texture is the best fur, of chinchilla.","(Uh oh, uh oh, uh oh, oh no no)","Been dealing with chain smokers,","But how you think I got the name Hova?","(Uh oh, uh oh, uh oh, oh no no)","I been realer the game's over,","(Uh oh, uh oh, uh oh, oh no no)","Fall back young, ever since the label changed over","(Uh oh, uh oh, uh oh, oh no no)","to platinum the game's been wrap, One!","Got me looking, so crazy, my baby","I'm not myself, lately I'm foolish, I don't do this,","I've been playing myself, baby I don't care","'Cuz your love's got the best of me,","And baby you're making a fool of me,","You got me sprung and I don't care who sees,","'Cuz baby you got me, you got me, so crazy baby","HEY!","Got me looking so crazy right now, your love's (oh love)","Got me looking so crazy right now (lookin' crazy)","Got me looking so crazy right now, your touch","Got me looking so crazy right now","Got me hoping you'll page me right now, your kiss (baby)","Got me hoping you'll save me right now (baby)","Looking so crazy in love's, (whoa!)","Got me looking, got me looking so crazy in love. (whoa!)","Got me looking so crazy right now, your love's","Got me looking so crazy right now (your love)","Got me looking so crazy right now, your touch","Got me looking so crazy right now (your touch)","Got me hoping you'll page me right now, your kiss","Got me hoping you'll save me right now","Looking so crazy in love's,","Got me looking, got me looking so crazy in love.","Mission one","I'ma put this on","When he see me in the dress I'ma get me some (hey)","Mission two","Gotta make that call","Tell him get the bottles poppin' when they play my song (hey)","Mission three","Got my three best friends","Like we do it all the time we gonna do it again (hey)","Mission four","Got the vintage Rolls","Drop a couple hundreds tell him leave it at the door","I ain't worried doing me tonight","A little sweat ain't never hurt nobody","While you all standin' on the wall","I'm the one tonight","Getting bodied, getting bodied, getting bodied, getting bodied","Want my body","Won't you get me bodied","You want my body","Won't you get me bodied (hey)","Can you get me bodied","I wanna be myself tonight","Can you get me bodied","I wanna be myself tonight","Don't you see my body?","I want to let it out tonight","Wanna party, wanna dance, wanna be myself tonight, me bodied","Mission five","Skip to the front of the line","Let me fix my hair up 'fore I go inside (hey)","Mission six","Gotta check these chicks","'Cause you know they gone block when I take these flicks (hey)","Mission seven","Gotta make my rounds","Given eyes to the guys now I think I found him (hey)","Mission eight","Now we conversate","And we can skip small talk let's get right to the chase (hey)","You should see my body","I gotta know enough to know if you can get me bodied","I'm kinda tight, I'm feeling right enough to see somebody","I wanna let it off tonight","Wanna dance, wanna party wanna be myself tonight","Baby all I want is to let it go","Ain't no worries, oh","We can dance all night","Get me bodied","That means come closer to me","While we grind to the beat","And your body's touching my body","All I need is to let it be","Ain't no worry, no","Boy dance with me","Feel my body","Don't stop just come closer to me","While we grind to the beat","With your body touching my body","Get somebody","Ain't no shame 'cause I gotta get mine","I swing my hair, kick off my shoes","Come her boy let me work on you","I remember when you use to take me on a","Bike ride everyday on the bayou (You remember that? We were inseparable)","And I remember when you could do no wrong","You'd come home from work and I jumped in your arms when I saw you","I was so happy to see you (I was so excited, so happy to see you)","Because you loved me I overcome","And I'm so proud of what you've become","You've given me such security","No matter what mistakes I know you're there for me","You cure my disappointments and you heal my pain","You understood my fears and you protected me","Treasure every irreplaceable memory and that's why","I want my unborn son to be like my daddy","I want my husband to be like my daddy","There is no one else like my daddy","And I thank you for loving me","I still remember the expression on your face","When you found out I'd been on a date and had a boyfriend (My first boyfriend, you should have seen your face)","I still remember I caught you crying cause of my tattoo","Could have said Beyonce I told you so","Instead you said you'd get one too (Even my mama said y'all get one just like mine)","Words can't express my boundless gratitude for you","I appreciate what you do","You've given me such security","No matter what mistakes I know you're there for me","You cure my disappointments and you heal my pain","You understand my fears and you protected me","Treasure every extraordinary memory and that's why","I want my unborn son to be like my daddy","I want my husband to be like my daddy","There is no one else like my daddy","And I thank you for loving me","Even if my man broke my heart today","No matter how much pain I'm in I will be okay","Cause I got a man in my life that can't be replaced","For this love is unconditional it won't go away","I know I'm lucky","Know it ain't easy","For men who take care of their responsibilities","Love is overwhelming","Lord why did you pick me","Can't stop my tears from falling","I love you so much daddy","(Thank you, you've done so much for me. I love you daddy.)","I get so emotional daddy, every time I think of you","I get so emotional daddy, every time I think of you","There is no one else like my daddy","No one else replace my daddy...","Certified quality","A dat da girl dem need and dem not stop cry without apology","Buck dem da right way  dat my policy","Sean Paul alongside  now hear what da man say  Beyonce","Dutty ya, dutty ya, dutty ya","Beyonce sing it now ya","Baby boy you stay on my mind","Fulfill my fantasies","I think about you all the time","I see you in my dreams","Baby boy not a day goes by","Without my fantasies","I think about you all the time","I see you in my dreams","Aah oh my baby's fly baby oh","Yes no hurt me so good baby oh","I'm so wrapped up in your love let me go","Let me breathe stay out my fantasies","Ya ready gimme da ting dat ya ready get ya live","And tell me all about da tings that you will fantasize","I know you dig da way me step da way me make my stride","Follow your feelings baby girl b/c they cannot be denied","Come check me in-a night and make we get it amplified","Me have da ting to run da ship cause I'm go slip and I'm go slide","And in the words of love I got ta get it certified","But I give you da toughest longest kinda ride  girl","Baby boy you stay on my mind","Fulfill my fantasies","I think about you all the time","I see you in my dreams","Baby boy not a day goes by","Without my fantasies","I think about you all the time","I see you in my dreams","Picture us dancin real close","In a dark dark corner of a basement party","Every time I close my eyes","It's like everyone left but you and me","In our own little world","The music is the sun","The dance floor becomes the sea","Feels like true paradise to me","Baby boy you stay on my mind","Fulfill my fantasies","I think about you all the time","I see you in my dreams","Baby boy not a day goes by","Without my fantasies","I think about you all the time","I see you in my dreams","Baby boy you stay on my mind","Baby boy you are so damn fine","Baby boy won't you be mine","Baby boy let's conceive an angel","Top top  girl","Me and you together is a wrap  dat girl","Driving around da town in your drop top  girl","You no stop shock  girl","Little more da dutty, we'll rock dat world","Top top  girl","Me and you together is a wrap  dat girl","Driving around da town in your drop top  girl","You no stop shock  girl","Little more da dutty, we'll rock dat world","Baby boy you stay on my mind","Fulfill my fantasies","I think about you all the time","I see you in my dreams","We stepping in hotter this year,","We stepping in hotter this year,","I know you gon' like it,","I know you gon' like it.","I'm stepping in hotter this year,","I'm stepping in hotter this year,","So don't you fight it,","So don't you fight it,",
"To the left, to the left","To the left, to the left","To the left, to the left","Everything you own in the box to the left","In the closet that's my stuff","Yes, if I bought it, please don't touch","And keep talking that mess that's fine","But could you walk and talk at the same time","And, it's my name that's on that jag","So come move your bags, let me call you a cab","Standing in the front yard","Tellin' me, how I'm such a fool","Talkin' 'bout, I'll never ever find a man like you","You got me twisted","You must not know about me, you must not know about me","I could have another you in a minute","Matter of fact, he'll be here in a minute, baby","You must not know about me, you must not know about me","I can have another you by tomorrow","So don't you ever for a second get to thinking","You're irreplaceable","So go ahead and get gone","Call up that chick and see if she's home","Oops, I bet you thought, that I didn't know","What did you think I was putting you out for","Because you was untrue","Rollin' her around in the car that I bought you","Baby drop them keys","Hurry up before your taxi leaves","Standing in the front yard","Tellin' me, how I'm such a fool","Talkin' bout, I'll never ever find a man like you","You got me twisted","You must not know about me, you must not know about me","I could have another you in a minute","Matter of fact, he'll be here in a minute, baby","You must not know about me, you must not know about me","I can have another you by tomorrow","So don't you ever for a second get to thinking","You're irreplaceable","So since I'm not your everything","How about I'll be nothing","Nothing at all to you","Baby I won't shed a tear for you","I won't lose a wink of sleep","'Cause the truth of the matter is","Replacing you is so easy","To the left, to the left","To the left, to the left (mmmmmm)","To the left, to the left","Everything you own in the box to the left","To the left, to the left","Don't you ever for a second get to thinking","You're irreplaceable","You must not know about me, you must not know about me","I could have another you in a minute","Matter of fact, he'll be here in a minute, baby","You must not know about me, you must not know about me","I can have another you by tomorrow","So don't you ever for a second get to thinking (baby)","You must not know about me, you must not know about me","I could have another you in a minute","Matter of fact, he'll be here in a minute","You can pack all your bags","We're finished","'Cause you made your bed","Now lay in it","I can have another you by tomorrow","Don't you ever for a second get to thinking","You're irreplaceable","5, 3, 2011, let's move!","Clap your hands now!","Clap your hands now!","Clap your hands now!","Clap your hands now!","Jump, jump, jump!","Jump, jump, jump!","Jump, jump, jump!","Jump, jump, jump!","Mission 1,","Let me see you run,","Put your knees up in the sky,","'Cause we just begun, hey!","Hey!","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Mission 2,","This is how we do,","Shuffle couple to the right,","To the left, let's move!","Hey! Hey!","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Mission 3,","Can you dougie with me?","Throw your own lil swag on the swizzy beat,","Hey! Hey!","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Mission 4,","If you're ready for more,","Jump rope, jump rope,","Lift your feet off the floor,","Hey! Hey!","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","I ain't worried doing me tonight,","A little sweat ain't never hurt nobody,","Don't just stand there on the wall,","Everybody just move your body,","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Move your body,","Move your body,","Move your body,","Move your body,","Everybody,","Won't you move your body?","Everybody,","Won't you move your body?","Hey!","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Get me bodied,","I wanna be myself tonight,","Can you get me bodied,","I wanna be myself tonight,","Wanna move my body,","I wanna let it out tonight,","Gonna party, gonna dance, gonna be myself tonight,","Hey!","Mission 5,","Cumbia, let's go","Time to move your little hips,","Vamonos, Vamonos,","Hey! Hey!","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Mission 6,","Bring it back real quick,","Do the running man and then you turn around like this,","Hey! Hey!","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Mission 7,","Time to break it down,","Step and touch to the dancehall sounds,","Hey! Hey!","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Mission 8,","Feel that heart beat race","Snap your fingers, tap your feet,","Just keep up with the pace,","Hey! Hey!","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","I ain't worried doing me tonight,","A little sweat ain't never hurt nobody,","Don't just stand there on the wall,","Everybody just move your body,","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Move your body,","Move your body,","Move your body,","Move your body,","Everybody,","Won't you move your body?","Everybody,","Won't you move your body?","Hey!","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Get me bodied,","I wanna be myself tonight,","Can you get me bodied,","I wanna be myself tonight,","Wanna move my body,","I wanna let it out tonight,","Gonna party, gonna dance, gonna be myself tonight,","Hey!","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Fellas on the floor,","All my ladies on the floor,","Get me bodied, get ready, to move your body,","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Baby all I want is to let it go,","Ain't no worries, oh,","We can dance all night,","Move your body,","That means come closer to me,","While we dance to the beat,","Move your body,","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Now run to the left, to the left, to the left,","Now run to the left, to the left,","Now run to the right, to the right, to the right,","Run back to the right, to the right,","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Now run to the left, to the left, to the left,","Now run to the left, to the left,","Now run to the right, to the right, to the right,","Run back to the right, to the right,","(Jump, jump, jump, jump, jump","Jump, jump, jump, jump)","Wave the American flag,","Wave the American flag,","Wave the American flag,","Wave the American flag,","Hey!","Cool Off","Cool off","Cool off","Cool off","HEY!"]

texts = [[word for word in document.lower().split() if word not in stop] for document in our_texts]

dictionary = corpora.Dictionary(texts)







def data_cleanse(docs_to_clean):
	D=len(docs_to_clean)
	for d in range(0, D):
	    docs_to_clean[d] = docs_to_clean[d].lower()
	    docs_to_clean[d] = re.sub(r'[-\[\]]', ' ', docs_to_clean[d]) #ask 
	    docs_to_clean[d] = re.sub(r'[^a-zA-Z0-9 ]', '', docs_to_clean[d])
	    docs_to_clean[d] = re.sub(r' +', ' ', docs_to_clean[d])
	    docs_to_clean[d] = re.sub(r'\s\w\s', ' ', docs_to_clean[d]) #eliminate single letters
	return docs_to_clean

def create_model():
	data_cleanse(our_texts)


	"""gensim includes its own vectorizing tools"""
	corpus = [dictionary.doc2bow(text) for text in texts]

	model = models.LdaModel(corpus, id2word=dictionary, num_topics=number_topics, passes=10) #use gensim multicore LDA
	model.save('ldabey')
	model.show_topics()

	topics_indexed=[[b for (a,b) in topics] for topics in model.show_topics(number_topics,10,formatted=False)]
	topics_indexed=pd.DataFrame(topics_indexed)


	pp.pprint(topics_indexed)




model = models.LdaModel.load('ldabey', mmap='r')
model.show_topics()

import pandas as pd
topics_indexed=[[b for (a,b) in topics] for topics in model.show_topics(number_topics,10,formatted=False)]
topics_indexed=pd.DataFrame(topics_indexed)

topic_map = [[], [], [], [], [], [], []]


for o in our_texts:
	try:
		results = model[dictionary.doc2bow(o.lower().split()) ]
		value = max(results,key=itemgetter(1))[0] 
		topic_map[value].append(o)
	except Exception, e:
		continue


@app.route('/status', methods = ['POST'])
def getStatus():
	line = str(request.form['textmessage'])
	try:
		results = model[dictionary.doc2bow(line.lower().split()) ]
		value = max(results,key=itemgetter(1))[0] 
		message = random.choice (topic_map[value])
		#0-coquettish 1-coquettishplus 2-upset 3-dance 4-romance 5-angry 6-carefree
		if(value == 0):
			gif = 'coquettish'
		elif(value == 1):
			gif = 'coquettishplus'
		elif(value == 2):
			gif = 'upset'
		elif(value == 3):
			gif = 'dance'
		elif(value == 4):
			gif = 'romance'
		elif(value == 5):
			gif = 'angry'
		elif(value == 6):
			gif = 'carefree'
		return json.dumps({'message': message, 'gif': gif})
	
	except Exception, e:
		message = random.choice (our_texts)
		return json.dumps({'message': message, 'gif': 'default'})
	



# pp.pprint(topics_indexed)

if __name__ == "__main__":
  app.run(debug=True)