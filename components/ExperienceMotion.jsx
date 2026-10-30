'use client';
import {useEffect} from 'react';
import {usePathname} from 'next/navigation';
import Lenis from 'lenis';

export default function ExperienceMotion(){
 const path=usePathname();
 useEffect(()=>{
  const media=matchMedia('(prefers-reduced-motion: reduce)');
  let lenis,observer,mutation,raf=0;
  const animations=new Set();
  const main=document.querySelector('main');
  function setup(){
   if(media.matches)return;
   lenis=new Lenis({autoRaf:true,lerp:.085,smoothWheel:true,syncTouch:false,anchors:true,prevent:node=>!!node.closest?.('dialog,textarea,select,[data-lenis-prevent]')});
   observer=new IntersectionObserver(entries=>{for(const entry of entries){if(!entry.isIntersecting)continue;const el=entry.target;const animation=el.animate([{opacity:0,transform:'translate3d(0,32px,0)'},{opacity:1,transform:'translate3d(0,0,0)'}],{duration:850,delay:Number(el.dataset.revealDelay||0),easing:'cubic-bezier(.22,1,.36,1)',fill:'backwards'});animations.add(animation);animation.onfinish=()=>animations.delete(animation);observer.unobserve(el)}},{threshold:.08});
   const tracked=new WeakSet();
   function scan(){main?.querySelectorAll('.section-top,.intro-grid,.story-index>a,.feature,.collection-card,.gallery-tile,.island-card,.quiz-panel,.reading-note,.article-copy>p').forEach(el=>{if(tracked.has(el))return;tracked.add(el);if(el.matches('.collection-card,.gallery-tile'))el.dataset.revealDelay=String(([...el.parentElement.children].indexOf(el)%3)*75);observer.observe(el)});if(document.querySelector('dialog[open]'))lenis.stop();else lenis.start();}
   scan();mutation=new MutationObserver(scan);if(main)mutation.observe(main,{childList:true,subtree:true,attributes:true,attributeFilter:['open']});
   const parallax=()=>{raf=0;main?.querySelectorAll('.gallery-tile').forEach(el=>{const rect=el.getBoundingClientRect();if(rect.bottom<0||rect.top>innerHeight)return;const p=(rect.top+rect.height/2-innerHeight/2)/innerHeight;el.style.setProperty('--image-shift',`${Math.max(-15,Math.min(15,p*-22))}px`)})};
   const onScroll=()=>{if(!raf)raf=requestAnimationFrame(parallax)};
   lenis.on('scroll',onScroll);
  }
  function cleanup(){lenis?.destroy();lenis=undefined;observer?.disconnect();mutation?.disconnect();cancelAnimationFrame(raf);animations.forEach(a=>a.cancel());animations.clear();main?.querySelectorAll('.gallery-tile').forEach(el=>el.style.removeProperty('--image-shift'));}
  const change=()=>{cleanup();setup()};setup();media.addEventListener('change',change);
  return()=>{cleanup();media.removeEventListener('change',change)};
 },[path]);
 return null;
}
