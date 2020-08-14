function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded',()=>{
   let search= document.forms.search.elements.search
   search.oninput=async (e)=>{
       let response=await fetch('/find',{
          method: 'POST',
          headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken':getCookie('csrftoken')
          },
          body: JSON.stringify({string:e.target.value})
       })
       if(response.ok){
           let text=await response.text()
           
           if(text){
               console.log(text)
           }
       }
   }
})