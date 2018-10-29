// read settings file
let getData = () => {
    let json;
    $.ajax({
        async: false,
        url: "../static/js/settings.json",
        cache: false,
        dataType: "json",
        success: function(data){
            json = data;
        }
    });
    return json;
}

// settings.json
var settingsJson = getData();

var username        = settingsJson.credentials.regular_login.username;
var password        = settingsJson.credentials.regular_login.password;
var cardNumber      = settingsJson.credentials.library_login.card_number;
var cardPin         = settingsJson.credentials.library_login.card_pin;
var organizationUrl = settingsJson.credentials.library_login.organization_url;
var lyndaLocation   = settingsJson.preferences.location;
var downloadTime    = settingsJson.preferences.download_time;


// initialize variables onload
$(document).ready(function(){

    $('#username').val(username);
    $('#password').val(password);
    $('#card_number').val(cardNumber);
    $('#card_pin').val(cardPin);
    $('#organization_url').val(organizationUrl);
    $('#lynda_location').val(lyndaLocation);
    $('#download_time').val(downloadTime);

    // download method  
    $('#userPass-method').click(function(){
        settingsJson.credentials.course_download_pref = "regular-login";
    })    
    $('#cookies-method').click(function(){
        settingsJson.credentials.course_download_pref = "cookies";
    })

    // exercise file preferences
    $('#exfile-library-login').click(function(){
        settingsJson.credentials.exfile_download_pref = "library-login";
    })    
    $('#exfile-regular-login').click(function(){
        settingsJson.credentials.exfile_download_pref = "regular-login";
    })

    // use markdown links for chapters preferences
    $('#markdown-links-true').click(function(){
        settingsJson.preferences.markdown_links = true;
    })    
    $('#markdown-links-false').click(function(){
        settingsJson.preferences.markdown_links = false;
    })

    // download subtitles preferences
    $('#download-subtitles-true').click(function(){
        settingsJson.preferences.download_subtitles = true;
    })    
    $('#download-subtitles-false').click(function(){
        settingsJson.preferences.download_subtitles = false;
    })

    // download exercise files preferences
    $('#download-exfile-true').click(function(){
        settingsJson.preferences.download_exercise_file = true;
    })    
    $('#download-exfile-false').click(function(){
        settingsJson.preferences.download_exercise_file = false;
    })


    // choose web-browser to download exercise files
    $('#exfile-chrome').click(function(){
        settingsJson.preferences.web_browser_for_exfile = "chrome";
    })    
    $('#exfile-firefox').click(function(){
        settingsJson.preferences.web_browser_for_exfile = "firefox";
    })

    // choose exercise files download method
    $('#exfile-selenium').click(function(){
        settingsJson.preferences.exfile_download_method = "selenium";
    })    
    $('#exfile-aria2').click(function(){
        settingsJson.preferences.exfile_download_method = "aria2";
    })

    // redownload course
    $('#redownload-prompt').click(function(){
        settingsJson.preferences.redownload_course = "prompt";
    })    
    $('#redownload-force').click(function(){
        settingsJson.preferences.redownload_course = "force";
    })
    $('#redownload-skip').click(function(){
        settingsJson.preferences.redownload_course = "skip";
    })

    // aria2 installed?
    $('#aria2-true').click(function(){
        settingsJson.preferences.aria2_installed = true;
    })    
    $('#aria2-false').click(function(){
        settingsJson.preferences.aria2_installed = false;
    })


    // when SAVE button clicks
    $('button').click(function(){
        
        // update values
        settingsJson.credentials.regular_login.username         = $('#username').val();
        settingsJson.credentials.regular_login.password         = $('#password').val();
        settingsJson.credentials.library_login.card_number      = $('#card_number').val();
        settingsJson.credentials.library_login.card_pin         = $('#card_pin').val();
        settingsJson.credentials.library_login.organization_url = $('#organization_url').val();
        settingsJson.preferences.location                       = $('#lynda_location').val();
        settingsJson.preferences.download_time                  = $('#download_time').val();

        // send post request to api
        $.ajax({
            async: false,
            type: 'POST',
            url: '/update',
            data: JSON.stringify (settingsJson),
            success: function(data) { alert('data: ' + data); },
            contentType: "application/json",
            dataType: 'json'
        });
    })
  })

// Read download method state
if(settingsJson.credentials.course_download_pref == "regular-login") 
    document.getElementById('userPass-method').classList.add("active");
else
    document.getElementById('cookies-method').classList.add("active");
   
// Read exercise file download preferences
if(settingsJson.credentials.exfile_download_pref == "regular-login") 
    document.getElementById('exfile-regular-login').classList.add("active");
else
    document.getElementById('exfile-library-login').classList.add("active");

// Read markdown links for chapters state
if(settingsJson.preferences.markdown_links == true)
    document.getElementById('markdown-links-true').classList.add("active"); 
else
    document.getElementById('markdown-links-false').classList.add("active"); 

// Read subtitles state
if(settingsJson.preferences.download_subtitles == true)
    document.getElementById('download-subtitles-true').classList.add("active"); 
else
    document.getElementById('download-subtitles-false').classList.add("active"); 

// read download subtitles state
if(settingsJson.preferences.download_exercise_file == true)
    document.getElementById('download-exfile-true').classList.add("active"); 
else
    document.getElementById('download-exfile-false').classList.add("active"); 

// read exercise file state
if(settingsJson.preferences.web_browser_for_exfile == 'chrome')
    document.getElementById('exfile-chrome').classList.add("active"); 
else
    document.getElementById('exfile-firefox').classList.add("active"); 

// read exercise download method state
if(settingsJson.preferences.exfile_download_method == 'selenium')
    document.getElementById('exfile-selenium').classList.add("active"); 
else
    document.getElementById('exfile-aria2').classList.add("active"); 

// read redownload course state
if(settingsJson.preferences.redownload_course == "prompt")
    document.getElementById('redownload-prompt').classList.add("active");
else if(settingsJson.preferences.redownload_course == "skip")
    document.getElementById('redownload-skip').classList.add("active");
else
    document.getElementById('redownload-force').classList.add("active");

// read aria2 state
if(settingsJson.preferences.aria2_installed == true)
    document.getElementById('aria2-true').classList.add("active"); 
else
    document.getElementById('aria2-false').classList.add("active"); 

function toggleEye(textField, icon){
    passwordField = document.getElementById(textField);
    eyeIcon = document.getElementById(icon);

    if(eyeIcon.classList[1] == 'fa-eye-slash'){
        // closed eye
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');
    
        // change input type
        passwordField.type = "text";

    }
    else{
        // open eye
        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');
    
        // change input type
        passwordField.type = "password";
    }    
}