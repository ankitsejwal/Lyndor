
var settingsJson = getData();

document.getElementById('username').value = settingsJson.credentials.regular_login.username;
document.getElementById('password').value = settingsJson.credentials.regular_login.password;
document.getElementById('card_number').value = settingsJson.credentials.library_login.card_number;
document.getElementById('card_pin').value = settingsJson.credentials.library_login.card_pin;
document.getElementById('organization_url').value = settingsJson.credentials.library_login.organization_url;

document.getElementById('lynda_location').value = settingsJson.preferences.location;

// Read subtitles
if(settingsJson.preferences.download_subtitles == true){
    document.getElementById('download-subtitles-true').classList.add("active"); 
}else{
    document.getElementById('download-subtitles-false').classList.add("active"); 
}

// Download subtitles
if(settingsJson.preferences.download_exercise_file == true){
    document.getElementById('download-exfile-true').classList.add("active"); 
}else{
    document.getElementById('download-exfile-false').classList.add("active"); 
}

// Exercise file
if(settingsJson.preferences.web_browser_for_exfile == 'chrome'){
    document.getElementById('exfile-chrome').classList.add("active"); 
}else{
    document.getElementById('exfile-firefox').classList.add("active"); 
}

// redownload course
if(settingsJson.preferences.redownload_course == "prompt"){
    document.getElementById('redownload-prompt').classList.add("active");
}else if(settingsJson.preferences.redownload_course == "skip"){
    document.getElementById('redownload-skip').classList.add("active");
}else{
    document.getElementById('redownload-force').classList.add("active");
}

// aria2
if(settingsJson.preferences.ext_downloader_aria2_installed == true){
    document.getElementById('aria2-true').classList.add("active"); 
}else{
    document.getElementById('aria2-false').classList.add("active"); 
}

function getData(){
    var json;
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