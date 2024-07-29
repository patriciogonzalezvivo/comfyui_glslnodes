import { app } from '../../scripts/app.js'

export function makeUUID() {
    let dt = new Date().getTime()
    const uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = (dt + Math.random() * 16) % 16 | 0
        dt = Math.floor(dt / 16)
        return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16)
    })
    return uuid
}


/**
 * Calculate total height of DOM element child
 *
 * @param {HTMLElement} parentElement - The target dom element
 * @returns {number} the total height
 */
export function calculateTotalChildrenHeight(parentElement) {
    let totalHeight = 0
  
    for (const child of parentElement.children) {
      const style = window.getComputedStyle(child)
  
      // Get height as an integer (without 'px')
      const height = Number.parseInt(style.height, 10)
  
      // Get vertical margin as integers
      const marginTop = Number.parseInt(style.marginTop, 10)
      const marginBottom = Number.parseInt(style.marginBottom, 10)
  
      // Sum up height and vertical margins
      totalHeight += height + marginTop + marginBottom
    }
  
    return totalHeight
  }
  

export const removeLastUniform = (node) => {
    let last_index = node.inputs.length - 1;
    let last_input = node.inputs[last_index];
    if (last_input.name.startsWith("u_") || last_input.name === "...") {
        node.removeInput(last_index);
    }
}

export const removeAllUniforms = (node) => {
    let totalInputs = node.inputs.length - 1;
    for (let i = totalInputs; i >= 0; i--) {
        if (node.inputs[i].name.startsWith("u_") || 
            node.inputs[i].name === "uniforms" ||
            node.inputs[i].name === "vertex_code" ||
            node.inputs[i].name === "3D model"
        ) {
            node.removeInput(i);
        }
    }
}

export const getMaxIndex = (node, str) => {
    let maxIndex = -1;
    for (let i = 0; i < node.inputs.length; i++) {
        if (node.inputs[i].name.startsWith(str)) {
            maxIndex = Math.max(maxIndex, parseInt(node.inputs[i].name.replace(str, "")));
        }
    }
    return maxIndex;
}

export const getNextName = (node, str) => { return str + (getMaxIndex(node, str) + 1); }

export const addInput = (node, index, str, type, unique=true) => {
    let name = str;

    if (unique) 
        name = getNextName(node, str);
    
    node.graph.beforeChange();
    
    node.inputs[index].name = name;
    node.inputs[index].type = type;
    
    node.addInput("...", "*");
    node.graph.afterChange();
}


export class Vector {
    constructor (vec, type) {
        this.value = [0,0];
        this.dim = 2;
        this.set(vec, type);
    }

    set (vec, type) {
        if (typeof vec === 'number') {
            type = type || 'vec2';
            this.set([vec], type);
        }
        else if (typeof vec === 'string') {
            let parts = vec.replace(/(?:#|\)|\]|%)/g, '').split('(');
            let strValues = (parts[1] || parts[0].replace(/(\[)/g, '')).split(/,\s*/);
            type = type || (parts[1] ? parts[0].substr(0, 4) : 'vec' + strValues.length);
            let values = [];
            for (let i in strValues) {
                values.push(parseFloat(strValues[i]));
            }
            this.set(values, type);
        }
        else if (vec) {
            if (Array.isArray(vec)) {
                this.value = [];
                this.value.length = 0;
                this.dim = type ? Number(type.substr(3, 4)) : vec.length;
                let filler = vec.length === 1 ? vec[0] : 0;
                for (let i = 0; i < this.dim; i++) {
                    this.value.push(vec[i] || filler);
                }
            }
            else if (vec.dim) {
                this.value = vec.value;
                this.dim = vec.dim;
            }
        }
    }

    set x (v) {
        this.value[0] = v;
    }

    set y (v) {
        this.value[1] = v;
    }

    set z (v) {
        if (this.dim < 3) {
            while (this.dim < 3) {
                this.value.push(0);
            }
            this.dim = 3;
        }
        this.value[2] = v;
    }

    set w (v) {
        if (this.dim < 4) {
            while (this.dim < 4) {
                this.value.push(0);
            }
            this.dim = 4;
        }
        this.value[3] = v;
    }

    get x () {
        return this.value[0] || 0.0;
    }

    get y () {
        return this.value[1] || 0.0;
    }

    get z () {
        return this.value[2] || 0.0 ;
    }

    get w () {
        return this.value[3] || 0.0;
    }

    // VECTOR OPERATIONS
    add (v) {
        if (typeof v === 'number') {
            for (let i = 0; i < this.dim; i++) {
                this.value[i] = this.value[i] + v;
            }
        }
        else {
            let A = new Vector(v);
            let lim = Math.min(this.dim, A.dim);
            for (let i = 0; i < lim; i++) {
                this.value[i] = this.value[i] + A.value[i];
            }
        }
    }

    sub (v) {
        if (typeof v === 'number') {
            for (let i = 0; i < this.dim; i++) {
                this.value[i] = this.value[i] - v;
            }
        }
        else {
            let A = new Vector(v);
            let lim = Math.min(this.dim, A.dim);
            for (let i = 0; i < lim; i++) {
                this.value[i] = this.value[i] - A.value[i];
            }
        }
    }

    mult (v) {
        if (typeof v === 'number') {
            // Mulitply by scalar
            for (let i = 0; i < this.dim; i++) {
                this.value[i] = this.value[i] * v;
            }
        }
        else {
            // Multiply two vectors
            let A = new Vector(v);
            let lim = Math.min(this.dim, A.dim);
            for (let i = 0; i < lim; i++) {
                this.value[i] = this.value[i] * A.value[i];
            }
        }
    }

    div (v) {
        if (typeof v === 'number') {
            // Mulitply by scalar
            for (let i = 0; i < this.dim; i++) {
                this.value[i] = this.value[i] / v;
            }
        }
        else {
            // Multiply two vectors
            let A = new Vector(v);
            let lim = Math.min(this.dim, A.dim);
            for (let i = 0; i < lim; i++) {
                this.value[i] = this.value[i] / A.value[i];
            }
        }
    }

    normalize () {
        let l = this.getLength();
        this.div(l);
    }

    getAdd (v) {
        var A = new Vector(this);
        A.add(v);
        return A;
    }

    getSub (v) {
        var A = new Vector(this);
        A.sub(v);
        return A;
    }

    getMult (v) {
        var A = new Vector(this);
        A.mult(v);
        return A;
    }

    getDiv (v) {
        var A = new Vector(this);
        A.div(v);
        return A;
    }

    getLengthSq () {
        if (this.dim === 2) {
            return (this.value[0] * this.value[0] + this.value[1] * this.value[1]);
        }
        else {
            return (this.value[0] * this.value[0] + this.value[1] * this.value[1] + this.value[2] * this.value[2]);
        }
    }

    getLength () {
        return Math.sqrt(this.getLengthSq());
    }
}


export class Matrix {
    constructor(m, type) {
        this.dim = 3;
        this.value = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]];
        if (m) {
            this.set(m, type);
        }
    }

    set (m, type) {
        if (m.value[0][0]) {
            this.value = m.value;
            this.dim = m.dim;
        }
        else if (m[0][0]) {
            this.value = m;
        }
    }

    rotateX (theta) {
        let c = Math.cos(theta);
        let s = Math.sin(theta);
        let T = [
            [1, 0, 0],
            [0, c, -s],
            [0, s, c]];

        this.value = this.getTransform(T);
    }

    rotateY (theta) {
        let c = Math.cos(theta);
        let s = Math.sin(theta);
        let T = [
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c]];

        this.value = this.getTransform(T);
    }

    getMult (v) {
        if (v[0][0] || (v.value && v.value[0][0])) {
            // TODO: what If v is a matrix
            console.log('TODO: what If v is a matrix');
        }
        else {
            // If v is a vector
            let A = new Vector(v);
            let B = [];
            for (let i = 0; i < A.dim; i++) {
                B.push(A.value[0] * this.value[i][0] + A.value[1] * this.value[i][1] + A.value[2] * this.value[i][2]);
            }
            return new Vector(B);
        }
    }

    getTransform (m) {
        let newMatrix = [];
        for (let row in m) {
            let t = m[row];
            let newRow = [];
            newRow.push(t[0] * this.value[0][0] + t[1] * this.value[1][0] + t[2] * this.value[2][0]);
            newRow.push(t[0] * this.value[0][1] + t[1] * this.value[1][1] + t[2] * this.value[2][1]);
            newRow.push(t[0] * this.value[0][2] + t[1] * this.value[1][2] + t[2] * this.value[2][2]);
            newMatrix.push(newRow);
        }
        return newMatrix;
    }

    getInv() {
        let M = new Matrix();
        let determinant = this.value[0][0] * (this.value[1][1] * this.value[2][2] - this.value[2][1] * this.value[1][2]) -
                            this.value[0][1] * (this.value[1][0] * this.value[2][2] - this.value[1][2] * this.value[2][0]) +
                            this.value[0][2] * (this.value[1][0] * this.value[2][1] - this.value[1][1] * this.value[2][0]);
        let invdet = 1 / determinant;
        M.value[0][0] = (this.value[1][1] * this.value[2][2] - this.value[2][1] * this.value[1][2]) * invdet;
        M.value[0][1] = -(this.value[0][1] * this.value[2][2] - this.value[0][2] * this.value[2][1]) * invdet;
        M.value[0][2] = (this.value[0][1] * this.value[1][2] - this.value[0][2] * this.value[1][1]) * invdet;
        M.value[1][0] = -(this.value[1][0] * this.value[2][2] - this.value[1][2] * this.value[2][0]) * invdet;
        M.value[1][1] = (this.value[0][0] * this.value[2][2] - this.value[0][2] * this.value[2][0]) * invdet;
        M.value[1][2] = -(this.value[0][0] * this.value[1][2] - this.value[1][0] * this.value[0][2]) * invdet;
        M.value[2][0] = (this.value[1][0] * this.value[2][1] - this.value[2][0] * this.value[1][1]) * invdet;
        M.value[2][1] = -(this.value[0][0] * this.value[2][1] - this.value[2][0] * this.value[0][1]) * invdet;
        M.value[2][2] = (this.value[0][0] * this.value[1][1] - this.value[1][0] * this.value[0][1]) * invdet;
        return M;
    }
}