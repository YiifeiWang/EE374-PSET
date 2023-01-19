import { canonicalize, canonicalizeEx } from 'json-canonicalize';

type taclass={
    ta: string;
    type: string;
}


export const build_taclass = (params: taclass) => {
return params;
};

let taobject = build_taclass({ta: 'Kenan',
type: "ta"})

let tajson = canonicalize(taobject);

console.log(typeof(tajson));

const isJsonString= (str:string) =>{
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
};


console.log(isJsonString(tajson));