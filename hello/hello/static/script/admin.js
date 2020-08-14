 $(()=>{
        form=document.querySelector('.form_user_create');

        
        document.querySelector('#adduser').addEventListener('click',(e)=>{
          document.querySelector('#adduser_box').classList.remove('none')
        })
        form.onsubmit=async(e)=>{
          e.preventDefault();
          let response = await fetch('/addnewuser', {
          method: 'POST',
          body: new FormData(form)
          });
          if(response.ok){
                 let json=await response.json()
                 document.querySelector('.errors_user').classList.remove('none')
                 for (let key in json) {
                    let li=document.createElement('li');
                    li.className="list-group-item list-group-item-primary"
                    li.innerHTML=json[key]
                    document.querySelector('.errors_user').append(li)
                 }
           
          }
        } 
        $('#create_post').click(()=>{
           $('.create_post').removeClass('none')
        })
   

 }) 
       
      