document.addEventListener('DOMContentLoaded',callme)
function callme(){
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
    
    let form=document.querySelector('.select__order')
    let price=document.querySelector('#price')
    price.onclick=async(e)=>{
        let sel=document.querySelector('.oneshot')
        if(!Number.isInteger(parseInt(sel.value))){
            $('#price-discounts').value="Должно быть число"
        }
        else{
            let response=await fetch(form.dataset.url, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'X-CSRFToken':getCookie('csrftoken')
                },
                body:encodeURI('count='+sel.value)
              })
        
            if(response.ok){
                let data=await response.json()
                $('.price-discounts').text=data
            }
        }
    }
    
}

