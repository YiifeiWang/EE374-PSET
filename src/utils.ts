import { canonicalize, canonicalizeEx } from 'json-canonicalize';

export type message_class={
    content: string;
    type: string;
}

export type hello_class={
    "type": string,
    "version": string,
    "agent": string,
  }

export type error_class={
    "type": string,
    "name": string,
    "message": string,
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