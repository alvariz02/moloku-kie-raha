import test from 'node:test';
import assert from 'node:assert/strict';
import {frameAt,FRAME_COUNT} from '../lib/scroll-frames.mjs';
test('scroll samples every frame forward and backward including both endpoints',()=>{for(let i=0;i<FRAME_COUNT;i++){assert.equal(frameAt(i/(FRAME_COUNT-1)).index,i)}assert.equal(frameAt(1).next,11);assert.equal(frameAt(.5).blend,.5);assert.equal(frameAt(0).index,0)});
test('invalid progress clamps and reduced motion holds first frame',()=>{assert.equal(frameAt(-1).index,0);assert.equal(frameAt(2).index,11);assert.equal(frameAt(NaN).index,0);assert.deepEqual(frameAt(.8,true),{index:0,next:1,blend:0})});
