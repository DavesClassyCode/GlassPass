function verifyUsername() {  
   var userName = document.getElementById("username").value;
   //check empty userName field  
   if(userName == "") {  
      document.getElementById("login-error-message").innerHTML = "Fill the username please!";  
      return false;  
   }  

   var regEx = /^[0-9a-zA-Z]+$/  
   if(userName.value.match(regEx)) {  
      document.getElementById("login-error-message").innerHTML = "Username must consist of letters or numbers only.";  
      return false;  
   } else {  
      alert("Username is correct");  
   }  
 }

function verifyPassword() {  
    var pw = document.getElementById("password").value;  
    //check empty password field  
    if(pw == "") {  
       document.getElementById("login-error-message").innerHTML = "Fill the password please!";  
       return false;  
    }  
     
   //minimum password length validation  
    if(pw.length < 8) {  
       document.getElementById("login-error-message").innerHTML = "Password length must be at least 8 characters";  
       return false;  
    }  
    
  //maximum length of password validation  
    if(pw.length > 15) {  
       document.getElementById("login-error-message").innerHTML = "Password length must not exceed 15 characters";  
       return false;  
    } else {  
       alert("Password is correct");  
    }  
  }


 function clearErrorMessage() {
   document.getElementById("login-error-message").innerHTML = "";
 }

 function validateLogin() {
   clearErrorMessage();
   verifyPassword();
   verifyUsername();
 }