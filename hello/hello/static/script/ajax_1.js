
     document.addEventListener('DOMContentLoaded',()=>{

      $('.user-menu__toggle').click(()=>{
        $('nav').slideToggle()
     })        

      let so=async()=>{
          let data = await fetch('/data');
          if(data.ok){
              let mydata=await data.json()
             
              for (let value of mydata){
                let pa_card=document.getElementsByClassName('special')[0]
                let card= pa_card.cloneNode(true)
                card.classList.remove('none')
                card.firstElementChild.src=value[0]
                card.children[1].firstElementChild.textContent=value[1]
                pa_card.parentElement.append(card)
              }
              document.querySelector('.news').classList.remove('none')
          }
     }
      so()
      let changecount=document.getElementsByClassName('somebutton')[0]
      let url=changecount.getAttribute('href')

      changecount.onclick=async()=>{
        console.log(url)
        let count=document.querySelector('#say_hy').value;
        console.log(count)

        if(!Number.isInteger(parseInt(count,10))) return;

        let response = await fetch(url.concat('/?count='+count));
        if(response.ok){
            document.querySelector('.amout_of').innerHTML=" Quantity:"+count
             
        }
      }
            


     })
     
   



   
  
