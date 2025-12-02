Hi guys, welcome to the session on coffee with PB and today we have a special guest Mr. Pushbinda Singh my
brother back to the channel and uh we did the two podcast together and it was amazing. He is a cloud security
architect with one of the bank and one of the rare professional who holds CCI with four AWS certification and SAPSA
CCSK and he recently cleared CCSP also. uh when you're talking about push
pushpender pushpender designing a zero trust architectures and they're aligning all the business with sapsa and also for
the finance and public sector clients and the best thing about this person is he turned the complex hybrid cloud
network into the clear riskbased architecture which is talk about security by design and you know economy
of mechanism which is called keep it simple and whether when he's not in hardening his AWS landing zone and all
that he do lot of social services he meant engineers on advancing from cloud network fundamentals to full full stack
cloud security. So let's welcome pushpender. It's really great honor for us to have him on this platform. Taking
out the time in weekend is not a small thing but it's a big big thing and thanks push by giving back to the
society and today topic I think we discussing about practical of threat modeling a first kind of video which
going to be live on YouTube very soon which talk about reality how the threat modeling works in the organization.
Yeah, thank you PR for having me and it's always a pleasure to be on your show. I do enjoy some of the podcasts
that you've done recently and I think the OT1 is really something that I'm
looking forward to but again it's a pleasure to be sharing this uh stage
with you and again there's no need of introduction to you. uh you're one of the mentors and the gurus that we look
forward to and something that I've learned from you is how to give back to the community. So this is my small uh
way of showcasing some of the knowledge and sharing it with our peers so that we can build a stronger security community
together. Thanks. Thanks. And guys, he's planning to start very soon YouTube channel on cloud security architect and all that.
Please do monitor properly and you will not miss uh the great insight coming
from the guy who practically implement cloud security. See we have a two type of people in the market. One is talk one
is talkative one is basically actionable and pushpender is a person who works on the actionable metrics. So his first
student will be today is prair and he sitting with his notes and all that and I will be speaking on behalf of the
students and viewers who have a lot of question on threat molding. So pushandai what is special today what we are making
today what is cooking tonight okay so there's a lot cooking in in the
kitchen but for today what we wanted to do is bring threat modeling in a very simple
terminology to our viewers and give them an opportunity to understand the complexities behind a threat model
understand why it's easy and difficult to perform this and and understand how
someone can adopt a method methodic of understanding the approach of doing
threat model. See the complexity with threat model is it's designed to provide the
organization or an individual with a view to say what needs to be protected,
how it needs to be protected and in what fashion it needs to be protected.
Organizations these days value business and business is driving uh where and how
they open up opportunities, right? So for example, if you talk about financial
organization, they are doing a lot more into AI. They
are trying to bring new technology, new products, new ventures every day.
However, as an architect, having a tool in your pocket or as a security
practitioner having a tool in your pocket which defines a framework of how you bring your existing controls into
play and how you protect the organization in different landscapes and
environments is very critical and threat modeling is a tool that helps you in
that journey because you can attach it to the development cycle. you can define
those controls and make sure that the security becomes an enabler for the
business rather than being uh called out as a showstopper. Right? So we want to
help the business grow so that we can grow along with it. Right? Okay. So
one thing that viewers have to understand is threat modeling is not just a tool that you can run and it
spits out information. It's an idea in your brain. It's like practicing maths.
The more you do it, the better you get at it, the faster you are and the more efficient you are. So understanding the
basics really helps you define how and in what way an organization can be
at risk. Where in a system are those weak points? what kind of defense and
depth do I need to plug those gaps and where sometimes security can be an
additional overhead to the business right and that's really important because
these days the margins are very thin so business really wants to know why am I
implementing something and is a blanket rule sufficient enough or should I have
very specific categories and controls in play Right? So you no longer just define
and say, "Hey, should I just encrypt everything?" Yes, you can. That would provide you a
lot more security. Encryption as a matter of fact is one of the strongest
controls in security. But you can't use this as a sword wielding around and
cutting everybody with it. Right? Imagine an application that has 10 different uh points where encryption can
be performed. Now if you ask the application to encrypt each and every payload every time it goes in and out,
you will hamper the business because the application rather than processing 10,000 requests a minute will only
perform five and that's no good to the business. an overly secure system is an
hindrance to the organization and uh hampers the productivity. Right? So
that's where defense and depth is good but we also need to keep in mind that
just enough security is the right mindset that ties back with zero trust.
Right? Okay. So we want terminology. So just enough security is
a great thing to keep in mind. That is where the best value for the business is
from a security pro. So these days the expectation from a security practitioner
be it a security architect, enterprise security architect or a security engineer whatever role you're performing
the business looks at you and asks you a very important question. How do you help
me protect my environment in the most efficient way possible? I don't want to
layer controls over controls over controls that either make it very
difficult for me to perform a function or make it make my system so
overburdened that we have to either spend more in terms of capacity to make
that function at an acceptable level or leave some controls out because it's
practically bringing the application down. Right? So that's where it is important to understand how can I figure
out what's sufficient for a system and to do that we've got a great methodology
which is threat modeling right today in this session we're going to focus more
on the stride methodology however please note that there are different variations
and versions of it pasta dread are some of the other versions but they define
and cate categorize in different functionalities and some of these can be used in tandem. Some of my viewers would
be interested in AI and as we all know with the advent of new things security
also keeps up and we've also got a new framework called Maestro that is used
for threat modeling AI systems. However, what we need to understand is that the
groundwork remains the same. So the basic process in each of these remains
the same. How you measure and get those valuable outputs can differ slightly but
it would depend on what is the outcome that you're looking for. In stridebased
what we know is we can figure out what are our threats where are they where are
the weak points or exposure points in a system and what kind of risk are we open
to so I'll quickly share my screen so that the viewers can get a visual of
what we are talking about I'll walk you through very simple stride definitions
what they essentially mean in terms of risk and what as a security pro uh we
should focus on and then I'll walk you through an example or couple of example one generic which I know a lot of
viewers would have seen in other YouTube videos but what we are bringing today in
this podcast is very valuable that we will break down one sample system that
everybody would have seen or can connect to in as a visual and then showcase what
kind of controls in a real life scenario that you can implement and someone who's
maybe starting off as a new security architect or a security engineer or if you're in sock all of these
different uh profiles can benefit from understanding how this flow would work
for a very basic application. Understood? Right. So, stride threat modeling uh or threat
modeling in general is a systematic approach for identifying, analyzing and
applying controls that mitigate security threats in a system or a design. Now
when we say a system and specifically word design, what we want to say is that
this is an activity that should be performed way in advance when you're
designing a system. So don't try and do a threat model when you've already rolled out a system. It's practically
too late and the cost of then baking in security is going to be exponentially
high. However, we know that developments these days follow
an agile or a waterfall approach. However, if you look at realistically,
many organization follow a merged model which is partially waterfall, partially
agile, which means that your threat models have to be very adaptive. So
every time there is a change in the design and a specific functionality of
the design, a threat model may be warranted for the organization depending on how much has changed. But what has
specifically changed in a system is very critical for analyzing threat model
and a key factor there is data flows. So we always as security practitioner
need to remember that data is what provides value to the organization and
where data flows is where we need to see the controls are appropriate. Right? So
imagine Coca-Cola has their IP in their secret source of how they make their
drinks and that is data which is the core value of the business. If we can't protect
their IP the organization loses its edge as a result it will go out of business.
So always remember that data flows are important to understand where valuable
data is moving within the organization. A simple example is an organization has
public facing information, generic information. An organization will have
its own IP. If it's a financial organization, it may host and store PI
or card information. True. Now these are different categories of data. Now if I was to be a security
architect and say let's secure everything with a blanket rule and encrypt everything. I don't want even a
single system to be able to decrypt it. A it's too much security. B it's not
appropriate security for different flavors of information. So categorizing
data is important. understanding where the data is flowing primarily the one
that is of high sensitivity is critical. So I would want to ensure
that my card information like PIN if I was to look at PCI DSS those uh kind of
standards would define should I be encrypting PIN and yes the PIN needs to
be encrypted even when it is flowing in an encrypted channel. So I'm looking for
something called payload level encryption but it is costly to implement it. So I can't be payload level
encrypting everything that flows from a user to my application or my back end.
Right? So that's where data flows are really important for us to understand.
Right? So what is threat modeling and why should I care about it? Threat
modeling is an approach which helps us proactively right that's why I said
don't do it at the last stage where your application is like do it more upfront
in your development cycle so proactively figuring out vulnerabilities
you help define and design where key security control integration would be in
your architecture and then you define and answer some key questions
And these questions are what am I building right? What is the organization
trying to build? Is it a public facing website or am I building an application that allows customer to store capture
card information right so depending on what am I building I would know what's
the criticality of the app what kind of data it has and then on top of that I
need to know what can go wrong right if my application is only internal having a
control that protects it from let's say DO is sometimes irrelevant, right? Because
I don't have that exposure. So why put DOS as a control when it's not needed?
So that's where we need to know what can go wrong and then you need to answer as a practitioner what should we do about
it. So when I know that I have a public facing website that's prone to denial of
service, what do I have as a control in my organization that can protect me? Now
that can control can be a layered control let's say network firewall if I
talk about cloud you have NSGS subnet level control VPCs micro segmentation
uh some form of CDN that can do DDOS prevention right so that's where
layering comes into play but then we need to understand as architects or practitioners what do we have and what
should I do about that risk And then lastly when we have baked in or
understood or proposed to the uh project or whatever application is being
developed we need to understand have we done a good job and it's more than a question. This is
what makes threat modeling an iterative exercise right. You do it once. Take put
it through a feedback loop. Understand the controls are effective. Has the project changed. Have have their
deliverables changed? Initially they might have been making a internal facing
application but then suddenly the application team might turn around and say hey I want to integrate with the
third party. Now they are public facing. I need to integrate with the SAS.
They are public facing. So now your entire architecture has evolved right so
you need to factor in those additional security controls and that's where we need to ask ourel have we done a good
job or not okay right now key thing that this helps us
perform is get more confidence in security get more confidence towards
security being an enabler because what we are doing is we are communicating our requirements early on to the project.
Now, no one wants to do a bad job, especially our engineers who are developing stuff.
The problem comes that they know of the requirements very late in their journey.
So, when you're already under pressure of delivering something with tight timelines, helping the business move
faster, you can't have requirements delivered to you at the last minute.
Mhm. So it's like if I was starting to build a car with four wheels and nobody told
me the XL should be four wheels and not three wheels and if I've designed for
three wheels then it's more of an auto than a car. Right? So you need to
understand the requirements have to be defined early on and same is the case
with security. Right? So you need to tell people or or an application do you want to do
oorthth? Do you need people to do o or do you need the application to support
oorth so that the entire infrastructure supports it?
Then let's dive into something called the stride model that I've spoken about.
So what does stride means? It has but pushander before uh I'm sorry to interrupting you here. when it come to
the threat modeling can if you go back to the previous slide where you discuss about the pointers about uh uh the
functions and all that I have one question here is okay the company sent a requirement we want to build an
application and we decided we need to do threat modeling fine what are the important documents
see when when we teaching CSSP or when you're talking about lot of speakers we say threat modeling is should be done in
security by design or shift left and all that but I have one question here is
apart from DMD document what are the other stuff is required when you're building a threat modeling you know a
starting point what are the artifacts is required and what are the mistake people does when they go for threat modeling
uh that's a great question and actually the kind of artifact depends on how
mature the organization is I've been in different places where uh
it's gone through just a rough diagram somewhere someone scrabbling on a piece
of paper to an organization where you've got dedicated uh frameworks in place um similar to how
a solution architecture is and that's where a security architect would capture
what they capture is really important. So for an effective threat model you
need to understand what are the critical components of an application and those
then that then need to be defined into an architecture or a breakdown into
several categories. So I'm going to show you later on how some of those categories are, but in essence the
important aspects of a threat model or a
security architecture document that you would see in a very refined organization
like financial services would be a design or asis state of what the
architect has reviewed or assessed. So when you talk to domain architects or
people who are defining and designing the application, they would have for
instance today an architecture design which is version one and it can quickly
evolve into five different versions. So you would have different versions of the same artifact. The architecture would
have moved. So it doesn't really make sense for security to have assessed version one when you're implementing
version five. So getting a state or capturing the state of the architecture
that's been assessed is really important. It also helps you with audit
and later on compliance relevance as well because you know what you have done
and is a key artifact that can be given to auditors as well to for them to
understand what kind of controls you have defined. Now within this diagram or
the architecture that you capture another important aspect is a ensuring
that you have captured all different elements which means defining what are
the key aspects of the architecture. Do you have external users? Do you have
internal users? Is the application in DMZ? Is it sitting in your internal
network? So all of those are key aspects of the architecture. Okay. One thing that people miss is labeling.
So make sure that you label and tag all the relevant components in your
architecture. Now once you've done that that is where you capture your stride model and define
for each element within the architecture what are the applicable security gaps or
controls and then what is the recommendation. Now I've seen mature organization create
this into an a list that's then given to the projects to either review and also
put in information and it can act as your risk register as well or a feed
into your risk register. Sometimes organization want to do the right thing but you may have difficulty with
technology compatibility issues but this is a great way to understand what was
the risk that you had what was the control you wanted to implement and then
did you find challenges in implementing that control okay right so an example real life example
that I can give you is sometimes projects when they work in cloud right they want to leverage
key management but within the organization if you don't
have a solidified way of or a defined pattern or a blueprint around how do I
store keys how do I generate keys can I share keys between application can I
share a key with a third party if so where will the vault live is it my
subscription third party subscription what are those patterns right if you have not develop those sometimes it's
very difficult to use that off the bat right so as a result this becomes a very
good tool for you to say where are some of my blueprints or capabilities missing
and then it becomes a very good feed into your security architecture to say I've got 15 projects that are going into
cloud but they don't know how to encrypt and securely pass data so key management
is a critical blueprint that we should develop Right? So it becomes a key validation
for you to say where are some of my gaps as well. Right? So again feedback into
the risk register again capturing all those information. Of course whenever it's a official document you should be
able to capture the scope and what's out of scope as well. Right? Okay. So those
are key information that should go into a welldefined threat modeling document
and also understand that it's a live document. Unless your architecture is
implemented, this will always be reiterated. So if you've got version one
captured today and there's a version five of the application or something in the architecture has changed, this will
be updated. So making sure that you've got good documentation governance around
capturing when states have changed has that been acknowledged it's coming from a refined source it's matching what's
being implemented is really important right so don't underestimate the power
of a good threat modeling document right it's very critical and
that is the reason I asked this question is u you know when we're talking about
uh uh threat modeling and all that everyone say okay data flow diagram should be there or something else will
be there but the most important part here is um how do you integrate what is the
steps what is the step-by-step process that's something people are missing so that's the reason I asked that question
so before we yeah so before I move to the next point like you know before we move to the next
slide here is if I ask about five artifacts we should look or in in just
one minute you know this this this. So what are those five artifacts or six artifacts?
Okay. So whenever you do a threat model summary is uh look for scope. Make sure
you call out out of scope uh definitions. Uh make sure you capture the data flow.
Make sure you define your trust boundaries. Understand where those uh risk would be.
uh then it's in my opinion very important to label stuff and make sure
that they define what exactly is mentioned in the artifact and then uh
you also need to have one format where you're doing stride or whatever your
threat model is and defining the risk plus the mitigation
why how we decide the threat modeling okay we are going for stride fine we have a pasta also
We have DSHA also. We have Italy also. We have multiple. But why we should go for stride not for pasta?
Good question. That's an organizationbased decision. Usually what
you would see is stride is really easier for you to bifurcate and implement in
architectures. pasta if you look at it or dread in that case their versions are
different in terms of the output that they're giving. So dread for example tells you
some of the risk factors and it revolves majority around the risk. Can this be
compromised? Where are my risk and all those things? Stride is more structured
in the sense that it tells you what kind of mitigation and controls you would need. Right? So there are organization
that have their own versions of threat modeling as well u which is a
combination of multiple things right but in organization if you've got a good risk framework
putting stride in is much more easier and it's one of the better used models
if I were to say more adopted so it's much more common to see this and people
having more acceptance around this as well understood Thank thanks for asking that thanks for
answering that question because it is a question normally asked by fellow people and all that you know there's so many
noise is there so that's why to cut out those noise that's why I asked that question thanks thank you so much
all right uh we will move forward with the stride model so
stride again uh the uh composition is again has six categories So S stands for
spoofing which means you are impersonating someone or
being uh perceived as someone else or trying to be perceived as someone else.
Right? So impersonate user a process or a system that's really
important. Sometimes we see impersonation uh as being hey just a
being presented as B. No, it can be a process or a system as well, right?
Especially important with agent to a agent uh and agent take AI today where
um a lot of the authentication um is being questioned around how would
it scale when you've got layers of layers of system calling each other and how do you identify it's the right
person or or right system or not. Um second one is tampering. Tampering as
the word indicates you are trying to fiddle or change necessarily some
information or modify. In this case the information can be data, it can be code
or the system configuration itself. Right? So tampering can can have multiple layers with it. Then you've got
repudiation which is denial of action of performing something. Right? So it's
like a kid when their parents ask, "Have you eaten chocolate?" and they outright
refuse, right? But the only way to identify is if they've got some chocolate sticking on their teeth and
right. So repudiation is when someone tries to uh uh say that they haven't
done or performed a certain action, right? Yeah. um information disclosure is
unauthorized access to confidential or sensitive information and then denial of service. I think this
is one that most of the people are aware of is when you've got u a system that is
so busy that it becomes unavailable due and cannot process legitimate access.
Right? Uh I recently was having a discussion with one of my friend where
usually uh the denial of service is when you look at it security
practitioner think about DDoS as the only method of denial of service. Right?
M but there are multiple different ways and one of the examples that my friend
was talking about was where if you make one service
but with legitimate users as well make that service unavailable is also a
denial of service. Right? So it it was an interesting concept around DDoS not
being the only way for denial of service but there are other ways where legitimate usage of a service can be
denied. Elevation of privilege is when you try and get higher permissions or rights
into a system to do authorized work that you're not supposed to. Right? So it's
very simple that you're trying to do more than what you are uh provisioned to
do. So you're trying to elevate your privileges. Now I've talked about data flows a lot.
I just wanted to give a visual representation to our users in terms of how data flow looks like for a very
basic webfacing application. So if an application has but if you can little bit zoom it.
Yeah. So I think controls. Uh yeah yeah yeah it worked. Yeah. Thank you.
Okay. So a very simple webf facing application will have three different
components. It needs to have some form of database to store information or
perform any kind of activity or actions. And then it has because it's a public
facing web app, it would have some users or actions. Now this is just very simple
uh data flow where a user would do an input or an actor will try and do an
input to a web facing application and then that input can then go and be
stored into a database. So the architecture is very simple. There are three elements within this. Right? Now
here all of us would see okay users when they're talking to an application would
want some form of authentication and authentication service may need to have some form of credentials and then the
other aspect would be that external actors are on the outside layer or the
untrusted boundary and then you would have a internal network boundary as well because a web application can be sitting
in a DMZ and then you can have an internal application or an internal component that would be talking to the
database. Right? So external entities here are user system or services that
are outside of your control. There are processes in place that perform certain
functionality. This is the core or the core or the
IP functionality that an organization develops. It more or less handles the
compute portion of the application. Then you've got data stores. These define
what kind of database files, repositories as well as what level of
data are you carrying. So criticality of the data that's something that we spoke
about. And then the final thing is data flow which is to capture the movement of
data within the application. Where is it going to? How is it going? Where did it
come from? M now at this point we also can flow into something called a threat model flow. So
remember in security and in general for an organization
things start with risk and things end at risk. So what I mean by that is risk
defines should an organization do something. Will it create value or is it
creating more risk? Now as a financial or If I decide to today uh go and open a
bank in let's say Germany and I'm operating in Australia.
Now I need to know if the value of operating in Germany would be greater
than the risk I'm taking by moving there and the risk is I'm opening up myself to
different regulations. uh I am opening up my myself to different kind of uh regulatory
requirements, confidentiality requirements, uh overseas operations, how would I
handle that? People, process, technology, all of that would have to be layered. Now that's where for security
as well in terms of threat model having a view of risk is really important
because at the end of the day all it boils down to is can I get the risk
within the appetite of the organization. If I am then the controls are sufficient
unless there is a deviation or a failure in the control that I have implemented.
Okay. So this is a very simple model where if you look at a system, the system holds or
has data and data is as we've said is what is valuable to the organization. So
data is what creates value for the organization and value is what we need
to protect. Now systems create functionality, right? So a system
will give you a tool to do something. A system will allow you to log on. A
system will allow you to process something. A system is the one that
exposes certain kind of functionality. And this functionality can have
weaknesses or flaws and those can be then exploited. So what we are trying to
do is the system exposed functionality is what we want to protect from flaws
and those vulnerabilities are the exposure factors that we have got right.
So a threat to that vulnerability is the risk that we've got in the
organization. So if I know what kind of threats I have, having an understanding of the
weakness or the vulnerability in the system, I can layer my controls to
define what level of mitigation is required and how then how I can lower
the risk. Right? So this diagram is courtesy of a very good book that I read
on threat model and the book by the name of uh threat modeling uh and it's
designed for engineers threat modeling designed for engineers I I'm not
remembering the name of the author but we can put that in the description or the links if someone is keen go and have
a look at that book it's really nice and it dives into a lot more of these kind
of flows. Right? So keeping this in mind, the idea for performing stride or
any other uh threat model is to identify what risk I have, what are the threat
actors and then where are the vulnerabilities or weakness in my system. Right? So based on that you can
define how we would be uh layering our security controls and then providing
sufficient coverage to the organization uh from a security standpoint. So
keeping that risk in mind right uh what we want to do is understand the next
layer which is the trust boundaries right so now with data flow if you see
we've mapped a very basic design of where our elements are in terms of the
architecture we need to know where these elements are residing which means are
they in internal to our organization. Let's say an application talking to a
database is all internal. An internal user talking to an application is also internal. But if you
have a customer talking to your public facing application that is on the
internet boundary. Now the names do not matter. How you perceive this and
standardize this in the organization is important. Right? So if you've got five different architects who name this
differently is fine as long as this boundary or the associated controls stay
stagnant or static. And what I mean by that is if I got internet boundary
it captures external users coming to a web server which is an exposed endpoint
to the internet. Right now then you've got DMZ boundary and you
can see that the boundary is helping me with the flow. So it's telling me that
external users hit an exposed endpoint of a web server. Now this web server is
in my DMZ boundary and that is then talking to my application server. And
then you would have a different boundary which is internal network and application servers talking to database.
Now some organization have formal ways of calling these boundaries differently.
Right? So someone can call this internal network, private network, uh secure
network, anything doesn't matter. The important aspect as I said is what is
communicating, where is it communicating and how much control do you have on this
section of your environment or network. Right? Okay. So for example,
if I have an application that's contacting the database or the server, I
have control where this application can talk to. I've also got control on the database where this can talk to and whom
it can talk to. Right? So that means I'm controlling both aspects of it. Whereas
if I look at this aspect, I'm only as a
provider exposing my web server. I can't control if an external legitimate user
tries to connect to it or an adversary or someone with malicious intent tries
to contact with it. Right. So one of the key reasons for defining these
boundaries is to understand what is the level of control I have on the consumer
and the provider. Right? So if you see consumer here is uh external user
provider is web server. I can only control web server side. I can't go to the uh user and say hey please have
antivirus on your machine because someone can maliciously take over your machine and you access my web portal and
you can cause me harm right I can't do that because that's not in my control
but if I am doing application server to database I can make sure the application
is running on a hardened server I can make sure that the application only connects via HTTPS I can make sure that
the application is using strong credentials stored somewhere in secret
manager to call this database right so all of those things I can control on
both side so that's the relevance of trust boundary it also tells me where
some of these very specific controls are applied and have to be enforced right so
for example when traffic is coming from external to DMZ said I know it's a
firewall that would be in place right and it has to be a little permissive
firewall to the sense that I can't say only IP address X can connect if I have
a public facing website of course it needs to allow a whole wide internet to connect maybe some geollocation
restrictions can be there but majority of it it has to be wide open because if
I'm providing service to everybody in the world I can't tell them you can't
connect to me but I'm giving you service you have to open it right so that's where when you move
between trust boundaries even though you can have the same control the definition
of that control and enforcement can change and that's why knowing these boundaries is important another example
is that firewall that was open to everybody
when it's protecting the web server is going to have a similar rule for when
traffic moves from DMZ to internal network as well. Okay, we'll have a firewall here
but that firewall will have only limited traffic allowed. It would only say web server talking to
this application, right? Even though it's catering to the same flow but by
definition because it's protecting a different boundary the configuration has to be appropriate
to where the control is implemented. Right? So that's why knowing these boundaries is really critical for you in
the architecture. Right? Okay. Uh so I'm just going to skip this because we've already discussed that. Uh
so based on the threat model definition right if we were to plot it for a very
simple ecommerce application knowing what are thread boundaries and
data flow are you would always have consumers right these are the actors in
our definition and consumers can cause
normal traffic accepted acceptable traffic. They can also cause nuisance
which is social engineering, SQL injection, session hijacking. So let's
say it's a consumer with a malicious intent. They want to know if I can hack into your uh banking application and
make it uh maybe pay out $10,000 to some malicious
account, right? So they want to make or abuse your application and that is what
generates risk for us right that a user with malicious intent but e-commerce
platform that we've got as an organization holds customer data and you remember we
we had the application or the platform in the medium section which was
exterality right so this is what that application is So e-commerce platform
has data. What kind of data it has? It has customer data, payment data, order
history, anything else related. And that data is what creates business or value.
Right? Knowing customers can transfer information or pay for something, they
can order something online is the business value that you're providing. Think about Amazon, right? Unless you
can purchase something on their website, they're not going to make money. True. That's the business value. And business
value informs security. What needs to happen?
What do I need? Where do I need protection? Like if it's an e-commerce
website, you can't put a firewall in front of my web server and allow only my
onremises network. Nobody's going to buy anything then because nobody can reach my website. Right? Now that's where
security knowing what the business value is. What are we protecting? Create an
actual value. Right? And then how do I create a value?
I understand the weaknesses and layer those controls that can exploit the
vulnerabilities in my environment. Right? So wanted to break it down into a
more logical flow where people can understand what does that theory or that
threat model flow uh look like. Right now I've got a very simple example for
everybody.
So a lot of us use cars and I wanted to bring a general example of what's the
difference between driving or what's the risk or how do you do a threat model for
using a car that's for family purpose versus using a car that's run only in
formula ones. Right? So understanding the business value gives us a lot more
insights in terms of knowing what kind of controls we need to put in. Right? So
for example a family car it's environment that it's used in is it's
used in city street. It goes onto highways. It gets parked. You're trying to transport goods or groceries and
travel from one place to another. But a formula car is only run on racetracks,
right? It's not used for transporting goods. You only want to go from one place to another. Uh but as fast as
possible, right? And that place is usually isolated and you go in circles, right?
So the idea behind a family car, the real asset value to the family is that
it allows you to have a reliable mode of transport that takes you from one place
to another. It can help you do some of your daily activities patterns and that's important, right? At the same
time, a Formula 1 car is designed to go as fast as possible so that you win.
you're the first, right? So, it's designed for speed, performance, optimization,
right? It's designed to be reliable but light at the same time. So, they've got
very different use cases. Now, as a result of these different use cases,
because they've got different operating environment, they also have different controls and exposure factor. As a
result, the security mechanisms that are defined in these two cars or type of
cars are different. Now, let's look at some of the threats that we've got related to these two kind. Right? A
normal car that you use for your day-to-day activity is prone to theft.
You parked it somewhere, someone can try and break in. Right? But Formula 1 cars,
they're really protected with high value. you won't find them parked in any parking lot. So, as a result, theft is
not as big a concern here, right? Because it's not widely parked everywhere.
But accidents at the other hand are very common in
normal cars as well, but they are also applicable in your Formula 1 cars,
right? So, this risk can be common. Now unauthorized use is again something that
you are at risk in a normal car. Why? I want to take my car but my family member
would have taken it somewhere else or you could loan it to some someone else. You you've seen videos
where people try and steal the car keys and take it for a round. So that's
unauthorized use, right? But Formula 1 cars are have some protection against
it. You only get the steering and it's disconnected and once you put it in that's only when you can drive the car.
Right? So you can see the basic category or the value is the same. It's a car but
the functionality and how it's designed the purpose it's designed for is relatively different. As a result the
risk or the threats are relatively different. Right now, one aspect that
you would see is Formula 1 cars do not have a closed roof,
right? They want to keep it light. So, as a result, having a full roof does not make sense. Normal cars will have full
roofs. But what how does it impact us? Now, not
having a roof means that Formula 1 drivers wear a helmet.
Now, how many times have you seen a normal driver in a car wearing a helmet?
Yeah. When I go with people Yeah. You're protecting yourself against
a different risk. Yeah. Right. So accident and fatality in that
case can come from the person who's sitting next to you. Yes. But not because your car has been into
an accident. Right. So that's where you need to understand that because the risk of how the
architecture is of a Formula 1 car versus a normal car is different. The
control we have implemented is different. True. Now there's a different category or a medium category as well. There are
racing cars which are not Formula 1 but they are more refined version of
standard high performing cars that we've got and when people race in that the risk is higher of a crash as a result
you would see people wearing helmets in them as well. So if you're anytime doing high speed and it's not a normal car,
it's very okay for you to be wearing a helmet, right? But if you're using a standard car like a Kia or something and
then you're going on the road, it's not very common to have helmet on or especially on the driver. But what is
common, a seat belt is common. A seat belt is common in a Formula 1 car as
well as a standard car. But also you need to understand that how
security is provided also changes with how your threat or risk changes.
Now okay when you get into a crash in a normal car what do you see airbags deployed
the frame of the car is designed in a way that it can handle maximum of your
crash. You know what? Formula 1 cars are diff designed differently.
Because of the speed that they travel in, the car is actually designed to disintegrate
which mean it falls apart and the capsule is the strongest portion of the car. But if you see the moment it has an
impact a majority of the car like tires all of it will fall apart. Doesn't
happen in a normal car. So it's okay protecting both are protecting the person who's
driving human life but the way they are protecting is very different because how the functionality
is defined and how it so that's where how it is built. So that is why one of the principles of threat
modeling that we need to understand is different assets can be of the same
category face different complexities in different environment
right so as a result the control that you put in place can be different
in live example if you have on-pre you have a different control on the cloud you have a different controls
exactly but you could be protecting against the same risk. Yeah, that's true. Data loss or data
disclosures and all that. Exactly. So that is where you need to understand that risk in different
environment means different thing and when you change the environment a risk can change. As a result we said do the
threat modeling as a iterative process. It needs to be updated every time you go
through. Now all of us would have understood like the common threat model.
This is what uh PR you were talking about. So when you capture a document
right this is the summary of the threat model document that we can validate or
put um in in a standard format. Right? So as I said defining scope is really
important. Creating a DFD or a data flow diagram is
really important. Apply your stride model. Identify your threads weakness.
Do the risk assessment of saying why is this impacting me and then put in the
mitigations. These are really important to capture what needs to imple be
implemented to mitigate the risk and then if you can't implement something
link it to your risk register to say okay I can't implement this because of this and then this is also that feeds
into your enterprise security architecture or security architecture wall to say these are the blueprints or
the design or the patterns that we need to focus on. So really powerful this
kind of documentation and then you can also do validate and perform uh some
form of assurance around the effectiveness of the control. So let's say you've got a control that's
performing really well is a standard control in your organization like an
onremise. Now what if that key control is not applicable or irrelevant or not
available in your cloud environment? then that control is no longer effective. Right? So one example is your
onremises firewall. You can't have your public facing
firewalls also protect your uh cloud environment unless
unless you also host a similar functionality in your cloud and that's a
standard design or a pattern that you would see right unless you scale your solution or define that capability
someplace else that standard design or pattern may not be suff sufficient right
agree uh or may not provide you the best value. So you could opt to send all your
cloud bound traffic to onremises first and then use private link to send it to
the cloud. But that's an ineffective design, right? So reviewing the effectiveness of your solution,
understanding the effectiveness of the control and especially in changing times
like the adoption of AI, we need to be sure and uh aware is this protecting the
system in the intended way or not and is it apt for what we have started right
so the so one thing that I would want users to remember is from a thread modeling
perspective. Start early. Include everybody.
Save time, save cost, call out your requirements early, include different
stakeholders, talk to your architects, talk to the people who have proposed or
have the business requirement of the solution. So talk to business, talk to people who are building the solution,
your engineers. Tell them, share with them what you want. Give them details.
Don't assume that they know because not everybody wants to have the same mindset
or will have the same level of knowledge, right? So be an advocate for security. Keep models updated. So what
we mean by that is understand your mitigations. Look at them for the appropriateness. Ensure
that your models are up to date and they are providing or solving challenges or
use cases that your organization is looking to adapt. And then focus on the
high value assets. You can't do everything with only limited resources.
Yes. So make sure that you are protecting what is valuable to the organization and document any
assumptions or decisions. Right. So this is where the scope definition and
exclusions of the scope are really important. So anything that you have assumed make sure it's documented
because your assumption may have a big impact later on. Right.
I agree. So so don't assume and if you're assuming document it in in the register
get validations. So that's in a nutshell what you would want to do. and how you
would approach threat modeling. But this podcast wouldn't really be
theory a different different one if we were not going to show you a practical way of
doing it. So what I have done is we've created a tool a simple form or a format which
walks you through because as we said initially that this is more of a brain exercise. The more you do it, the better
you get. And the more examples you can walk through, not the hypothetical car
ones, but the real ones that you have in your environment, the better you get get
at implementing it. So, what I have is I've got a very simple application
that's designed to walk you through some of these steps, right? So, key concepts again, stride framework, spoofing,
tampering, repudiation, all of that is captured here. we've g given examples.
So understanding and bringing that bridging that knowledge is really easy
when you know how to correlate it with things that happen in or correlate it
with things that you know of right so trust boundary is there what I'm going to dive into is uh we've got this
effectiveness in terms of what makes the threat model really effective and this is just a summarized version of what you
would capture in the document that we've spoken about right so what I have in this tool is really simplest form of
an example which is to say you've got a e-commerce website right
and then these details can be as much as you want now the more you know the
better it is for you to figure out what kind of risk you would have but it's not
to say that it's not very good at a high level as well right so having bare bones
is also good but the more you know it the better and more apt the threat model
can be. So in this case you would see that I've given a very simple example of a e-commerce website that's using a
react front end very common NodeJS as the back end and then you've got a MySQL
database and a stripe payment because this is an e-commerce website so it's using some form of payment method. the
app right now as I said right very basic in the sense I've only captured a user
that needs authentication to a process which is doing sensitive data like PII
and payments so you've got a user element and a process element right the third only aspect is the data so if we
were to break this down into an architecture diagram how would that look
like from a threat modeling perspective perspective first thing I would document
is what do I have right so details of the website and this is where your
imagination and abstractions also come into play when you are starting off with
threat model it's really important to understand that the simpler you keep
your flows the easier it is for you to plot and define your requirements the
more complex you make it, the more difficult it is. Right? So, generalization initially is helpful.
That's when you start building into more complex one. Right? So, keeping it very simple. You've got a front end that
talks to a back end. You've got a back end that talks to a database database. You've got a back end that talks to your
payment gateway. Very simple. I've not complicated it by adding but but this is a very common common
practice which we we follow for every application. So make sure we have to define the static requirement in the page. Yeah.
Exactly. So that's that's correct. But what I'm trying to say is don't over
complicate it by adding elements like oh you've got a graph firewall you've got a firewall you've got a load balancer. All
of them can be added on later but this is just bare bones but for you to get
your thinking right and in the right direction. Now we said we've spoken a
lot about trust boundaries told the relevance of why it needs to be there. Now this is where it is in action. See
the naming convention doesn't really matter as long as you can consistently use it within the organization. Right?
Uh so we've got front end boundary which means untrusted clients to whatever your
client application is. Now as I said naming and labeling is really important.
Even though if I have two different architects using different boundary name as long as you can label and provide a
description it goes really well. It's very clear to me where am I going, how
am I going, what is the zone I'm operating in. You've got the backend boundary which is between your trusted
and you you remember I showed server to your database. You control both aspects.
It's a trusted environment, right? So, and then you've got payment gateway
boundary. This is external to your third party. So, you're talking to someone outside but from your trusted
application, right? Okay. So, so now what do I have is I
need to capture my data flow. Data flow as I said data is where the value of the
business is. So, I need to follow that trail to understand where I should be putting my controls. So, I've got a
front end that talks to the back end. So, this is one flow of data. And what
is the front end doing? It's user input of PII or credential. Someone making a
payment. they are putting in their personal information, card information and credentials. Backend to database is
the user data and order information like okay user is trying to buy this blah
blah blah and then you've also got the backend going to a payment gateway to validate the payment. You all see there
is a red redirection when you buy something in your app and then it goes to uh a payment gateway a third party
where they would ask for validation or something like that. Right? So now current data flows and now all of this
in an architecture diagram how does that actually look like? It would look
something like this. So you can draw this. This tool does it for you. But
what you can do is draw this similarly or use any other form. Use a tool of
your choice. People use draw.io a lot these days. Very simple. But what is
this is designed to do is captures that you've got a front end.
Again the red indicates that it has a very uh high exposure or risk because
it's in that front end boundary a boundary that we control portion of
right and then it moves into the backend boundary. So these outer layers are your
flows or trust boundaries that you've got and then these are the flows of traffic coming in and out. Right? So now
each flow can have its own stride map to it for you to understand where is my
risk and what do I need to do to mitigate that risk what kind of risk I
have. So for example if you see this database going back to the stride model
what do I have that is applicable? I can have repudiation going from back end to
database, right? Someone can try and make a change, unsolicitated change and
deny doing it, right? So I need to put a control around that. I could have
information disclosure. So database is holding information or the back end is
holding customer information that can be disclosed, right? So that's a an aspect
that I might need. Uh someone can tamper. So I could have a request that
the customer sent to this back end for maybe paying for one item. I can change
tamper with that request and maybe make it 100 items. Right? So tampering can happen. But what can't
happen here? Because this database is not exposed directly to an outbound
functionality. Can I do a DOS or denial of service to it
directly? No. No. Indirectly, yes.
Right. So that's where it is important to understand that it's initially easier
for you to just look at the direct correlation and risk. Sure. Indirect ones how we mitigate them? We
put controls where they're directly applicable. Right? Otherwise what happens is I've
seen some people when they are introduced to stride because it can
happen and there's no absolute they try and put all of the six categories in and
that's not scalable because if something is supposed to happen once every 100
times you might want to put a control in but something as a indirect correlation
can happen one in a 20 billion times do you really want to spend your time
trying to protect it. I don't know. Right. So that's where the real Yes. So
that's where the real value is that you start looking at the direct impacts.
Right? So that's why if you see the front end exposure to the back end, it
may have multiple or more categories. That's where you see denial of services
as a an example because this is the point where I have my exposure to the
internet. Now a lot of talk about this. Let's do the analysis. The tool actually
helps you do the analysis. Right? So we've tal spoken about the threats to
the front end uh from the front end to the back end. Right? So let's go and
look at spoofing. What is it that can happen or go wrong in spoofing? Spoofing, remember, stands for someone
impersonating you. So, a hacker can impersonate a user by
stealing credentials. True. Now, if someone loses their credentials,
that's a a a strong way for an hacker to get into the system and perform
malicious actions. Now, what do we do about it? If someone is stealing
credentials, we can have multiffactor authentication in place as well as secure session management. So session
management makes it difficult to steal credentials. But even if you have stolen
credentials using multiffactor authentication, allows you the capability for a hacker to not use just
the credential but they would have an outofband uh solution channel and all that. Yeah. uh channel
so that they can the system will validate is it coming from uh the true
user or not. Right? True. So that's the mitigation you can apply
for spoofing. Now there would be basic controls that this would rely on as well.
Right? So for example tampering is user modifying any input. Right? So what do
we do with tampering? We can validate inputs at server side also use signing
tokens for integrity. Right? So what we can do is we can uh use a mechanism like
HMAC for data integrity and also do input validation to make sure that
whatever the customer is publishing is what we are receiving. Right? So that's
how we could avoid tampering. We'll also look at something called information
disclosure. Now sensitive data which is the PI or the credential are can be
exposed in the flow from front end to back end. Now if I don't do TLS uh again
the uh this is asking for one 1.3 more
adopted these days but still a lot of organization are sticking to 1.2 and
it's still in use. But what we are actually saying is that if you do
encryption of the session yes and then what happens is that you
can prevent from sensitive data leak. Now this encryption can also help you in
spoofing or protecting spoofing. How? If you've got an encrypted channel, it
makes stealing credentials a lot more difficult because they're not flowing in plain text.
Plain text. Yes. So you can see that there are layering of these controls but
certain controls have to be baked in to protect certain kind of uh risk within
the stride model that you True. Right. So now let's take an example of an
internal boundary but but how how it generated a data. So did did we feed any information or um
are we going to run something like that? um like because you add the information
in the scoping and then uh do you add any source or any
file into that? So in this case uh the user can either
leverage this example or what you can do is start your own as well which means
you can put in the information and uh browse the file. So if browse the file
you can put in your own architecture JPEG or something or you can also describe your architecture here. Now
description helps you define some of these but the real value is in these data flows. So I
can add an external user here. But what is the sample of the what is
sample data flow? We can add like if I want to add I can simply add anything like API integrate and all that. So
so what need to be added here? So data flow source this is usually the
entity or the element from where the flow would be fine destination is where that traffic is
going. Now I can do this at as a load balancer right if I wanted to be more specific
in this. Yes. So add to flow what this would do is it would create this entry for you in
this architecture. Okay. Understood. Now then what you can do is the tool has
baked in some boundaries and these boundaries define the level of control. Now what you could do is in
this case you can have a custom or a web boundary. Now if the boundary is default
it would layer the same controls on it. So trusted boundaries are these only. I
have added one more which is the web server boundary. What it would do is help you populate this architecture. Now
you can see that in the diagram you've got one more element coming in external
user coming to a load balancer. Right? This is where the more complex your
architecture is, the more and you can see that this has also labeled threads.
How did the threads get labeled? A where this user is B where this is because of
the trust boundary they sit in. Yeah. These are the relevant threads around this
in the architecture. Okay. Now when you start analyzing some of it
right uh so look at the payment gateway
boundary when your controlled application is talking to a third party. What kind of
risk do I have? Spoofing is a key risk for me.
How? Because crossing the boundary, someone can spoof or
go to this payment gateway on my behalf and ask for ask it to do a specific
transaction. Right now, that's a critical risk. Now if you
are especially a financial organization or anytime contacting a payment gateway
or any payment services you would want them to only perform
actions that you have authorized or on your behalf right not a third party or
someone else asking them to make the payment. So that's where spoofing is
really important or mitigating the risk of from spoofing is important. Now what
kind of control you would put in for spoofing? In this case we are saying
mutual TLS and validate cross boundary request.
Now why am I discussing this? So initially you saw that for a user when
we had spoofing which meant front end to back end spoofing was again a valid risk
but the control we had was around authentication right but this was more or less around
multiffactor authentication or at least having a form of authentication it could be oath if it doesn't exist
some form of customer identity access management which could be oath driven
any other form right okay but the same risk when it's at a
different boundary between different system will have a different mitigation
so you agree different bit the difference is that users can put in their credentials and
that can be then authenticated and you can have an MFA but what about application applications can't do
multiffactor authentication right so how do you defend spoofing so for
application or system to system the tool we have is mutual DLS you take my
certificate I get your certificate and then when we exchange information you
validate mine I validate yours right okay so we both define our identities and that mutual TLS is then a session
that both of us use as a secure form form of communication. So that way
ensuring that I do not end up talking to a third party that I don't know and you
don't talk end up talking to a third party that you don't know because they've got the certificate to provide
and say hey I am coming from a valid entity right so this is really important where we
said uh remember the rule that just enough security and apt security and apt
control so knowing what to implement where and how to mitigate what risk is
really important. Now you could also see that similar control of MTLS
can be used when it's within the same boundary. So there are controls in the
security architecture world that solve specific use cases. They solve
a challenge around spoofing in threat model. But they are also applicable when
a specific category of a system talks to a specific category of a system. Right?
So back into database you can see that there is no spoofing at all because we
said what can you do? Database is for entry right? Yeah. So
that's where it has different uh risk around repudiation. Of course, you want
to log all the user actions and timestamps so that tomorrow if you want to prove that it was a user generated
authentic request, that's what you would want to capture. Right? So this tool
gives you the capability to train your brain in terms of what can be those
risk. How do I figure out based on the trust boundary the risk I would have on
my system and then what kind of mitigation or controls do I have? I've
also tried to bake in some of the libraries that you would end up using
right so OS as application security
system management and SAM are more or less used. I am trying to figure out and
uh make nest also added to this so that you you can know what based on your
organization and the kind of library that you use that this could be relevant for you. Right? So
in fact uh if there is enough uh
people uh who would want to do it we're more than happy to run uh some live
sessions around this and then give access to the tool for people to play around. I do have three more sample use
cases. One which is defined around AI and AI systems. So that can be really
helpful for users to understand uh that operate in environments or organization
that are heavily trying to adopt AI but also making sure that security is doing
the right thing and we're able to perform some of these reviews in time.
So and the way you created this uh data and all the pointers whatever we have. So
one thing I want to ask you like you know like you have built this own application
for threat modeling. Yes. Okay. Uh and it's my uh own version of
how I envision it. Um so and it's not publicly available at this point but I'm
using it mostly for my internal use but more than happy to have sessions where I
can share it with individuals and and the company who does not have a diagram or the person who's aspiring
person and he want to drive the things and all that. So in that case uh how
they can do threat modeling if they don't have a documentations sorry if they don't have a tool.
So there are other paid and non-paid versions of different tools. Everybody
has different functionality. So you could go and look at Microsoft stridebased tool. There is one from OAST
as well. These two are free but they've got their own version of
complexities and basic understanding right okay my whole purpose of doing this was that
the license one you don't really get access to that freely and just for
testing purpose also the other ones had their own adoption so I wanted to create one very
basic one which a user who's just getting started started doesn't really need to learn the tool to learn threat
modeling. Okay. So the tool this tool in my opinion is
removing the complexities or the learning curve that you would get from
onboarding to a tool itself. Right? So that's been removed so that you have an
easier path to just learning threat model and building those scenarios and
models into your mind not to have a learning curve steep learning curve first for the tool and then the threat
model right which is counterintuitive because the reason of asking this question is not everyone uh not everyone
running a tool and all that. So yes, they will use Excel frameworks and all that to conduct this assessment. But
yeah, it can be a good starting point to try but this is really a great insight where you have talk about how the
integrations and all that we had. Yeah. And I I think it's high time like
organizations uh invest a lot in terms of
adopting tooling that provide better capabilities to architects, engineers.
But the sad state in some form for security is that we're still stuck with
Excel. Right. That's true. So the sooner we move out of Excel, there is a world beyond it where
automation as well as applicability of AI hopefully brings in enough agility in
the overall process that uh we start baking some of this and then follow the
journey with the developers. Right. Excellent. And I'll share a an example
that happened with me a while back was uh we did recommend certain feature
engineers to implement a certain control and one of the feedbacks they got was
hey I never had this in my Jira board and that stuck something uh in in my
brain was that for someone who lives in as developer who lives in u Jira they
talk about their sprints they capture everything there and that's the work
that they see for the next two weeks now if my work is not getting into their
board right uh it's difficult for them to implement and I can't blame them like
if I am in their shoes if someone doesn't tell me explicitly to do this I
might not do do it Right? And sometimes the problem not the problem but how
organizations are designed right you won't get to talk to everybody who's
developing or designing a feature. So the best you can do it is have
automation help you communicate your requirements to them in the form that
they consume. So this is where I feel like having automation and there's
upliftment around uh how developers deliver stuff and then how we can
communicate our requirements to them is really important right
and when we're talking about the segmentations and all that you know uh these integrations actually play a very
important role but thanks pushender it was a great insight it it gave the a
very good workflow about starting from things. See everyone talk about theory theory but no one talk of practical and
this is something you have shared about the practical insight and uh we are
looking forward for doing some live session also in threat modeling and those who watching this video if you
want to do one live session do let us know in comment box because we are planning a one two day session or one
day session on threat modeling where we practically demonstrate from zero to the
10 about how things work but trust me this is one of the great insight we thought and I'm sure this this content
will going to be definitely create a game changanger for architects, designers and all that who want to
understand threat modeling in more in detail. You actually give everything for free to be frank. Thanks. Thanks
Pashinder. Yeah, it's not mine to give away for free. It's knowledge that should have
the wider impact, right? So the more people can benefit from this, the better
we are, right? That's great. So this is all from our side team. Do let us know how do you
find this podcast in a comment box. And if you still new to the channel, do subscribe to the YouTube channel and
click on the bell icon to make sure you should not miss our future videos on a similar topic. Thanks. Thanks. Thank you
so much. Thank you bro for having me on. We'll have more sessions
for sure.