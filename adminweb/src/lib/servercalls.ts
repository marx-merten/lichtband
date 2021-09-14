import { browser, dev } from '$app/env';

export function getBaseUrl(): string {
	if (dev) return 'http://172.17.100.58/';
	else return '/';
}

export function fetch_api<T>(url: string, options: RequestInit = {}): Promise<T> {
	if (browser)
		return fetch(getBaseUrl() + url, options).then((response) => {
			if (!response.ok) {
				throw new Error(response.statusText);
			}
			return response.json();
		});
	else return new Promise((result) => result(null));
}

export function put_apiWithProgress<T>(url: string, data=undefined,method="PUT",progressCB:(progress:number)=>void): Promise<T> {
	return new Promise((result) => {
        if (browser) {
		const oReq = new XMLHttpRequest();
		oReq.open(method, getBaseUrl() + url, true);
        oReq.upload.onprogress=(ev)=>{
            progressCB((ev.loaded/ev.total)*100)
        }
		oReq.onload = function (oEvent) {
			// Uploaded.
            const response=JSON.parse(oReq.response)
            result(response)
		};
		oReq.send(data);
	} else result(null)
});
}

export function put_file(path: string, src: string | File): Promise<string> {
	if (browser)
		return fetch(getBaseUrl() + 'api/fs/file/' + path, { method: 'PUT', body: src }).then((response) => {
			if (!response.ok) {
				throw new Error(response.statusText);
			}
			return response.text();
		});
	else return new Promise((result) => result(null));
}

export function fetch_file(path: string): Promise<string> {
	if (browser)
		return fetch(getBaseUrl() + 'api/fs/file/' + path).then((response) => {
			if (!response.ok) {
				throw new Error(response.statusText);
			}
			return response.text();
		});
	else return new Promise((result) => result(null));
}
