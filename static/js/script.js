// Disable mouse wheel on number inputs
document.querySelectorAll('input[type="number"]').forEach(input=>{
    input.addEventListener("wheel",function(){
        this.blur();
    });
});

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor=>{
    anchor.addEventListener("click",function(e){
        e.preventDefault();

        const target=document.querySelector(this.getAttribute("href"));

        if(target){
            target.scrollIntoView({
                behavior:"smooth",
                block:"start"
            });
        }
    });
});

// Scroll to prediction result
window.addEventListener("load",()=>{
    const result=document.getElementById("prediction-result");

    if(result){
        result.scrollIntoView({
            behavior:"smooth",
            block:"start"
        });
    }
});

// Clear page on refresh
window.addEventListener("pageshow",(event)=>{
    const nav=performance.getEntriesByType("navigation");

    if(event.persisted||(nav.length&&nav[0].type==="reload")){
        history.replaceState({}, "", "/");
        window.location.href="/";
    }
});

// Counter animation
const counters=document.querySelectorAll(".counter");

counters.forEach(counter=>{
    const updateCounter=()=>{
        const target=+counter.dataset.target;
        const count=+counter.innerText;
        const increment=target/100;

        if(count<target){
            counter.innerText=Math.ceil(count+increment);
            setTimeout(updateCounter,20);
        }else{
            counter.innerText=target;
        }
    };

    updateCounter();
});

// Scroll to top button
const topBtn=document.getElementById("topBtn");

if(topBtn){
    window.addEventListener("scroll",()=>{
        if(window.scrollY>300){
            topBtn.style.display="block";
        }else{
            topBtn.style.display="none";
        }
    });

    topBtn.onclick=()=>{
        window.scrollTo({
            top:0,
            behavior:"smooth"
        });
    };
}

// Show loader
const form=document.getElementById("loanForm");

if(form){
    form.addEventListener("submit",()=>{
        const loader=document.getElementById("loader");

        if(loader){
            loader.style.display="flex";
        }
    });
}