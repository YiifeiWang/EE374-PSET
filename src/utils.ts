import { canonicalize, canonicalizeEx } from 'json-canonicalize';

export type message_class={
    content: string;
    type: string;
}

export const isJsonString= (str:string) =>{
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
};

export const make_message_json = (content: string, type: string) => {
    return canonicalize({content : content, type : type});
    };