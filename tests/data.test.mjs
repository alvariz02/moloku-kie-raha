import test from 'node:test';
import assert from 'node:assert/strict';
import {collection,questions,searchCollection} from '../lib/data.mjs';
test('combined filters and case insensitive search return matching culture',()=>{assert.deepEqual(searchCollection({query:' SOYA ',category:'Seni',place:'TERNATE'}).map(c=>c.id),['soya-soya']);assert.equal(searchCollection({query:'sasadu',category:'Kuliner'}).length,0)});
test('favorites filter respects saved IDs and ignores unknown IDs',()=>{assert.deepEqual(searchCollection({saved:['sasadu','unknown']}).map(c=>c.id),['sasadu']);assert.equal(searchCollection({saved:[]}).length,0)});
test('all detail routes have unique slugs and questions have valid answers',()=>{assert.equal(new Set(collection.map(c=>c.id)).size,collection.length);for(const q of questions)assert.ok(q.answer>=0&&q.answer<q.options.length)});
