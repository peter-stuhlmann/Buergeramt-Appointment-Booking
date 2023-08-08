# Bürgeramt Appointment Booking

> Note that this is not an officially supported script. 

If you need an appointment at Berlin's Bürgeramt (citizen's office), you have to be quick and patient. This Python script books you the next available appointment at a Bürgeramt.  
In order not to refresh pages by hand for hours and then be too slow in the appointment selection I wrote this little helper script.


## Getting started
Make sure Python is installed on your System:
```
python --version
```

Install dependencies:
```
pip install -r requirements.txt
```


## How to use
```
py booking.py --name "John Doe" --email "j.doe@example.com" --id "121151"
```

`--name` - Enter the first and last name of the person for whom the appointment is booked   
`--email` - Enter the e-mail address to which the appointment confirmation should be sent   
`--id` - Enter the ID of the service you want to book an appointment for, e.g. "121151" to apply for a passport.   
To find the matching ID, click on a service at [https://service.berlin.de/dienstleistungen/](https://service.berlin.de/dienstleistungen/). The number at the end of the URL is the ID. This script is not suitable for services that can be done online.


## Good to know

### Timeout: Too many attempts
The script tries to book an appointment until it is successful. This can take many attempts at times. Note that there is a security mechanism on the booking page that will timeout you for a short time if too many attempts have been made. In this case it would make sense to use VPN and change the location if necessary.


---
Developed by [Peter R. Stuhlmann](https://peter-stuhlmann-webentwicklung.de).
Licensed under the [MIT license](./LICENSE).