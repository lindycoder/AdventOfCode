

export function list<TGen extends Iterator<TReturn>, TReturn>(gen: TGen): TReturn[] {
    let arr: TReturn[] = []
    let result = gen.next();
    while (!result.done) {
        arr.push(result.value)
        result = gen.next();
    }
    return arr
}

export function* zip<T1 extends any[], T2 extends any[]>(arr1: T1, arr2: T2): Iterator<[T1, T2]> {
    for (let i = 0; i < arr1.length; i++) {
        yield [arr1[i], arr2[i]]
    }
}

export function transpose<T>(arr: T[][]): T[][] {
    if (arr.length === 0)
        return []
    return arr[0].map((_, col) => arr.map(x => x[col]))
}

export function distribution(arr: string[]): Record<string, number> {
    let dist = {};
    for (const item  of arr) {
        if (!(item in dist))
            dist[item] = 0
        dist[item] += 1 
    }
    return dist;
}
