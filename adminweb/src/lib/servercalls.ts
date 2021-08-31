import {  browser, dev } from '$app/env';

export function getBaseUrl():string{
    if (dev) return "http://172.17.100.43/"
    else return "/"
}

export function fetch_api<T>(url:string):Promise<T>{
    if (browser)
        return fetch(getBaseUrl()+url).then(response =>{
            if (!response.ok) {
                throw new Error(response.statusText)
            }
            return response.json()
        })
    else return new Promise( (result)=>result(null))
}

export function fetch_file(path:string):Promise<string>{
    if (browser)
        return fetch(getBaseUrl()+"api/fs/file/"+path).then(response =>{
            if (!response.ok) {
                throw new Error(response.statusText)
            }
            return response.text()
        })
    else return new Promise( (result)=>result(null))
}