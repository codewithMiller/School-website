const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const hdr=$('header.site'),nav=$('#nav'),btn=$('#menuBtn');
const setNav=o=>{nav.classList.toggle('open',o);btn.innerHTML='<i class="bi bi-'+(o?'x-lg':'list')+'"></i>';btn.setAttribute('aria-expanded',o)};
addEventListener('scroll',()=>hdr.classList.toggle('scrolled',scrollY>8),{passive:true});
btn.onclick=()=>setNav(!nav.classList.contains('open'));
$$('#nav a').forEach(a=>a.addEventListener('click',()=>setNav(false)));
addEventListener('keydown',e=>{if(e.key==='Escape')setNav(false)});

const dlg=$('#loginModal');
if(dlg){
  $$('[data-open-login]').forEach(b=>b.addEventListener('click',()=>{setNav(false);dlg.showModal();$('input',dlg).focus()}));
  dlg.addEventListener('click',e=>{if(e.target===dlg||e.target.closest('[data-close]'))dlg.close()});
}

$$('[data-slider]').forEach(s=>{
  const t=$('.track',s),go=d=>t.scrollBy({left:d*t.clientWidth*.8,behavior:'smooth'});
  $('[data-prev]',s).onclick=()=>go(-1);
  $('[data-next]',s).onclick=()=>go(1);
});

setTimeout(()=>$$('.alert').forEach(a=>a.remove()),4500);


/* NEWS CAROUSEL */

document.querySelectorAll('[data-news-carousel]').forEach((carousel) => {
    const track = carousel.querySelector('[data-news-track]');
    const slides = Array.from(track.children);
    const pagination = carousel.querySelector('[data-news-pagination]');
    const previous = carousel.querySelector('[data-news-prev]');
    const next = carousel.querySelector('[data-news-next]');
    const status = carousel.querySelector('[data-news-status]');

    if (slides.length <= 1) {
        carousel.querySelector('.news-carousel-controls')?.remove();
        return;
    }

    let currentIndex = 0;
    let autoplay;
    let isPaused = false;

    const reducedMotion = window.matchMedia(
        '(prefers-reduced-motion: reduce)'
    );

    // Create one indicator for every slide.
    slides.forEach((slide, index) => {
        const dot = document.createElement('button');

        dot.type = 'button';
        dot.className = 'news-carousel-dot';
        dot.setAttribute('aria-label', `Go to story ${index + 1}`);

        dot.addEventListener('click', () => {
            showSlide(index);
            restartAutoplay();
        });

        pagination.appendChild(dot);
    });

    const dots = Array.from(pagination.children);

    function showSlide(index) {
        currentIndex = (index + slides.length) % slides.length;

        track.style.transform = `translateX(-${currentIndex * 100}%)`;

        slides.forEach((slide, i) => {
            slide.setAttribute(
                'aria-hidden',
                i === currentIndex ? 'false' : 'true'
            );
            slide.inert = i !== currentIndex;
        });

        dots.forEach((dot, i) => {
            if (i === currentIndex) {
                dot.setAttribute('aria-current', 'true');
            } else {
                dot.removeAttribute('aria-current');
            }
        });

        status.textContent =
            `Story ${currentIndex + 1} of ${slides.length}`;
    }

    function stopAutoplay() {
        clearInterval(autoplay);
    }

    function startAutoplay() {
        stopAutoplay();

        if (isPaused || reducedMotion.matches) return;

        autoplay = setInterval(() => {
            showSlide(currentIndex + 1);
        }, 5000);
    }

    function restartAutoplay() {
        startAutoplay();
    }

    previous.addEventListener('click', () => {
        showSlide(currentIndex - 1);
        restartAutoplay();
    });

    next.addEventListener('click', () => {
        showSlide(currentIndex + 1);
        restartAutoplay();
    });

    // Pause while the visitor interacts with the carousel.
    carousel.addEventListener('mouseenter', () => {
        isPaused = true;
        stopAutoplay();
    });

    carousel.addEventListener('mouseleave', () => {
        isPaused = false;
        startAutoplay();
    });

    carousel.addEventListener('focusin', () => {
        isPaused = true;
        stopAutoplay();
    });

    carousel.addEventListener('focusout', (event) => {
        if (!carousel.contains(event.relatedTarget)) {
            isPaused = false;
            startAutoplay();
        }
    });

    // Pause when the browser tab is hidden.
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            stopAutoplay();
        } else {
            startAutoplay();
        }
    });

    // Respect the visitor's reduced-motion preference.
    reducedMotion.addEventListener('change', () => {
        startAutoplay();
    });

    showSlide(0);
    startAutoplay();
});
