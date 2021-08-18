let m = document.getElementsByClassName("alert");  // Return an array

setTimeout(function(){
   if (m && m.length) {
       for (let i = 0; i < m.length; i++) {
        m[i].classList.add('hide');
       }
   }
}, 2500);