export class NavRoute {
    constructor(
        public path: string,
        public segment: string,
        public label: string,
        public icon: string = undefined) { }
}

export interface ScrollCompleteEvent {
    left: number;
    right: number;
    top: number;
    bottom: number;
}
