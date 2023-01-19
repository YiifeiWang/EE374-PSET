const string1 = "Hello";
const string2 = "World";

import { canonicalize, canonicalizeEx } from 'json-canonicalize';

type taobject={
    ta: string;
    type: string;
}

taobject.ta  = "Kenan";
taobject.type = "ta";

tajson = canonicalize(taobject);

console.log(tajson);
