# Kalenda

FEATURES TO ADD
* Calendar Configs
    * Auto add to calendar (Default)
    * Approval First from calendar owner (Optional)
* Appointment Types
    * Set Valid Appointment Durations per type (15 mins, 30 mins, etc) 

TODO

* ~~Login with Google~~
* ~~Get Calender Events~~
* ~~Refresh Token Functionality for attach_google_token decorator~~
* ~~Improve Events view~~
*  ~~Do UI Follow Setting an appointment flow~~
    * Optimize for Mobile - Make Mobile responsive
* Use Google API to create Appointments
    * Start
    * End
    * Summary
    * Description - App Generated
    * All Day toggle
    * Timezone
    * ID
    * Status Confirmed
    * Attendees
* Backend - Follow Setting an appointment flow
    * Create CalendarProfile Model
        * Color
        * google_id
             
    * Create Appointment
    * Create Appointment Type
        * Location
        * Name 

* Create Calendar Blocks Model
    Can be used by Appointments
    - Types: Appointment or Unavailable
    - Start
    - End
* Create Appointment Model
    * CalendarProfile
    * Start
    * End
    * Description
    * All Day toggle
    * TimeZone
    * google_id (app generated)
        * characters allowed in the ID are those used in base32hex encoding, i.e. lowercase letters a-v and digits 0-9, see section 3.1.2 in RFC2938
        * the length of the ID must be between 5 and 1024 characters
        * the ID must be unique per calendar
    * Summary
    * Status
    * Attendees



# Setting an appointment

* ~~Choose Available Date~~

* VUE - Choose from available times
* VUE - Choose length of appointment

* VUE - Enter Details Form - (Email, Name, Contact Number)
* Vue - Confirm Appointment
* Success Page - (Show event details)
