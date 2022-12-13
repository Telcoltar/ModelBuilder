import { z } from "zod"
import { createOption, createOptionSchema, Option, None } from "../../Option"
 import { Example, ExampleSchema } from "./Example"

export class ExtendExample extends Example {
    number_prop: number 

    constructor(init: z.infer<typeof ExtendExampleSchema>) {
        super(init)
        this.number_prop = init.number_prop
    }

    static fromJSON(parsedJSON: any) {
        const validated = ExtendExampleSchema.parse(parsedJSON)
        return new ExtendExample(validated)
    }

    static getSchema() {
        return ExtendExampleSchema
    }
}

export const ExtendExampleSchema = ExampleSchema.extend({
    number_prop: z.number().lte(5),
})