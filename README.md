# Alexa-MyQGarage
Using the Alexa Skills Kit to control your Chamberlain MyQ garage door.

## Description
By using the Alexa Skills Kit and AWS Lambda, you can control your Chamberlain MyQ garage door through your Amazon Echo.
This code adapts [David Pfeffer's](https://github.com/pfeffed) unofficial [Chamberlain Liftmaster API](http://docs.unofficialliftmastermyq.apiary.io/) to a Python-based app you can use inside of AWS Lambda.

## Usage
1. Create an Alexa Skills Kit (ASK) app, using the intent schema, custom slot values, and sample utterances in this repo. Choose an invocation name like `my garage door`.
2. Replace `<MYQ_LOGIN_USERNAME>` and `<MYQ_LOGIN_PASSWORD>` in `main.py` with the username and password you created at Chamberlain, and substitute `amzn1.echo-sdk-ams.app.<your-alexa-skills-id>` with the ID of the ASK skill you created. The `APP_ID` should remain the same, it is Chamberlain specific and not specific to your MyQ account.
3. Create a zip file for Lambda with the following command  (you'll need it later in step 6):

        zip -r lambda-upload.zip main.py myq.py requests requests-2.9.1.dist-info

4. Create a new [AWS Lambda](https://console.aws.amazon.com/lambda/home?region=us-east-1) function in the _us-east-1_ (N. Virginia) 
region. At "Select a Blueprint," press the "Next" button to skip.
5. For the "Configure Triggers" page, click in the dotted box to show the triggers options, and select "Alexa Skills Kit." Click next to continue.
6. Configure the function by giving it a name, description, and selecting the "Python 2.7" runtime. For "Code Entry Type," specify the ZIP file "lambda-upload.zip" that you created in Step 3.
7. Change "Handler" to "main.lambda_handler", and use a "Create new role from templates" as your "Role".
8. Give your role a name, like "MyQRole", and choose "Simple Microservice Permissions." Leave "Memory" and "VPC" at their defaults, and give a timeout of "15 seconds," then click "Next". A new page will open. Verify your details, then click "Create function."
9. Modify your ASK skill with the [ARN](http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) of your newly created function.
10. Test your interactions with the ASK console. When you've got it working, try it on your Echo: `Alexa, ask my garage door to open`.

## If this worked, congratulations! If not, keep reading!
IMPORTANT:  Before attempting to troubleshoot your issue, first verify that AWS Lambda is fully up and running by checking its status on the [AWS Service Health Dashboard](https://status.aws.amazon.com/).

Troubleshooting Alexa to Lambda interactions can be done via AWS Lambda. The Lambda function panel will have tabs for Code, Configuration, Triggers, and Monitoring. "Monitoring" is where you can view logs to see the requests that come in from the Alexa Skills Kit. Most of the time, you'll be able to find the error here. A lot of times, you'll see errors because you didn't change some of the default values in the `main.py` code in lines 14, 15, and 24.

If you're still stuck, read the excellent [step-by-step guide](https://github.com/jbnunn/Alexa-MyQGarage/blob/master/StepByStepInstructions) from @tigerbrain.

### Alexa Skills Kit Documentation
The documentation for the Alexa Skills Kit is available on the [Amazon Apps and Services Developer Portal](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/).

### Resources
Here are a few direct links to Alexa and Lambda documentation:

- [Using the Alexa Skills Kit Samples (Node.js)](https://github.com/amzn/alexa-skills-kit-js)
- [Getting Started](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/getting-started-guide)
- [Invocation Name Guidelines](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/choosing-the-invocation-name-for-an-alexa-skill)
- [Developing an Alexa Skill as an AWS Lambda Function](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-lambda-function)

### Callouts

Special thanks to the contributors who help keep this alive. Check out [https://github.com/arraylabs/myq](https://github.com/arraylabs/myq) for some great work that keeps inspiring this project, and @tigerbrain's [Multi Door Support](https://github.com/tigerbrain/Alexa-MyQ-WithMultiDoorSupport) work.

### Disclaimer

The code here is based off of an unsupported API from [Chamberlain](http://www.chamberlain.com/) and is subject to change without notice. The authors claim no responsibility for damages to your garage door or property by use of the code within.
