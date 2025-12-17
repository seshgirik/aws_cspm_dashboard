## Lexus, a service that transcribes voice messages
This service provides the transcription API to Wxcas for transcribing voice mails recorded from Webex calling feature of Webex meetings. This service communicates with components like Voicea, Cxapi & U2C. Lexus is stateless service. No data is maintained by the Lexus service.

## client
It is used to invoke the rest endpoint of Lexus during integration test. It is also used by response client to communicate with the CXAPI server. The API exposed by this module is directly consumed by others, so be considerate when changing it.

## How to do.

### Setup the environment variables for lexus:
bootStrapServerProp: localhost:9092
bootStrapConsumerProp: localhost:9092

### ffmpeg setup.

#### Windows setup.
Step 1:
Download ffmpeg : https://ffmpeg.org/download.html

[Mirror link](https://github.com/GyanD/codexffmpeg/releases/download/2021-12-27-git-617452ce2c/ffmpeg-2021-12-27-git-617452ce2c-full_build.7z)

Step 2: 
Extract the zip and place the extracted file in to 'C://' drive.

Step 3: 
Set the path variable to the extracted bin folder, Path: C:\ffmpeg\bin

Step 4:
Open the command prompt and run ffmpeg to verify if the installation is completed. 

#### Linux setup

apt-get install ffmpeg

### Kafka setup locally

https://cisco.webex.com/cisco/ldr.php?RCID=714559fb5f256441432cfefad63c1d91

Password: wP6Jhcqv

### Run redis setup.

Download redis: https://redis.io/download

Run : Open cmd and run redis-server.exe

### LocalStack, you can run your AWS applications.

LocalStack is used only for testing - [reference](https://confluence-eng-sjc12.cisco.com/conf/pages/viewpage.action?pageId=241456545)

[LocalStack](https://confluence-eng-sjc12.cisco.com/conf/display/MESSAGING/CALL-45735+Explore+Localstack+to+simulate+AWS+S3+in+integration+environment)

### Security Rate limiting local setup

https://confluence-eng-sjc12.cisco.com/conf/display/MESSAGING/CALL+-44401+Security+Traffic+AND++Protocol+protection+for+Lexus+service++Denial+of+service

## PagerDuty

https://ciscospark.pagerduty.com/services/PZGV51T

## Logs

### Production

https://logs-noram.wbx2.com/app/kibana

`logs6aiad2-es-app:logstash-app-lexus` — to filter logs for Lexus

### Integration

https://logs-noram-int.wbx2.com/app/kibana

logs6aiad2-es-app:logstash-app-lexus` — to filter logs for Lexus

## Metrics

Integration | Production
------------|-----------
[Metrics Dashboard for Integration](https://metrics-noram-int.wbx2.com/d/CdLUiKSnz/lexus-dashboard?orgId=1) | [Metrics Dashboard for Production](https://metrics-noram.wbx2.com/d/CdLUiKSnz/lexus-dashboard?orgId=1)


## Deployments

Integration | Production
------------|-----------
intb1/intb3 (int-first) | a6,a7,a8 (achm) Chicago, USA
intb2/intb4 (int-second) | r1,r2,r3 (aore) Oregon, USA
&nbsp;|k1,k2,k3 (afra) Frankfurt, Germany


## Pipelines

- [Master Pipeline](https://sqbu-jenkins.wbx2.com/service06/job/team/job/lexus/job/pipeline/job/master/)
- [Deploy Jobs](https://sqbu-jenkins.wbx2.com/service06/job/platform/job/deploy/job/lexus/)
- [Test Jobs](https://sqbu-jenkins.wbx2.com/service06/job/platform/job/pipeline/job/public-test/job/lexus/)
- [Archive Jobs](https://sqbu-jenkins.wbx2.com/service06/job/platform/job/pipeline/job/team/job/lexus/)

## Threat Model
[ID 31921](https://wwwin-tb.cisco.com/www/threatBuilder.html?id=31921)

## Corona
[ID 82722](https://corona.cisco.com/releases/82722)
 
## TPS Compliance
[ID 1197420429](https://tpscompliance.cisco.com/compliance/product-releases/product/1197420429) 
