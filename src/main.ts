import {ExtendExample} from "./models/generated/ExtendExample";
import {union, z, ZodInvalidUnionIssue} from "zod"
import {ExampleSubType} from "./models/generated/ExampleSubType";
import {Example, ExampleSchema} from "./models/generated/Example";

const ex = Example.fromJSON({
    string_prop: "Hello",
    int_prop: 5,
    boolean_prop: true,
    float_prop: 5.6,
    option_string_prop: {
        is_some: true,
        value: "World!"
    },
    http_url_prop: "http://example.com",
    int_array_1_prop: [2,3],
    int_array_2_prop: [4,5],
    int_with_mod_prop: 12,
    string_array_prop: ["Hello", "World"],
    url_prop: "file://example.ftp",
    complex_array: [{string_prop: "Hello form subtype."}],
    date_prop: new Date("2012-01-01")
})

console.log(ex)
console.log(ex.option_string_prop)

try {
    const failed_ex = ExampleSchema.parse({
        string_prop: "Error",
        int_prop: 12,
        boolean_prop: true,
        float_prop: 5.6,
        option_string_prop: {
            is_some: true,
            value: 5
        },
        http_url_prop: "http://example.com",
        int_array_1_prop: [2,3],
        int_array_2_prop: [4,5],
        int_with_mod_prop: 12,
        string_array_prop: ["Hello", "World"],
        url_prop: "file://example.ftp",
        complex_array: [{string_prop: "Hello form subtype."}],
        date_prop: new Date("2012-01-01")
    })
}

catch (e) {
    if (e instanceof z.ZodError) {
        e.issues.forEach(issue => {
            if (issue.code == z.ZodIssueCode.invalid_union) {
                let union_issue = issue as ZodInvalidUnionIssue
                union_issue.unionErrors.forEach(err => {
                    console.log(err.issues)
                })
            } else {
                console.log(issue)
            }
        })
    }
}

const schema = z.union([
    z.object({
      is_some: z.literal(false),
      value: z.union([z.null(), z.undefined()])
    }),
    z.object({
      is_some: z.literal(true),
      value: z.string().min(5)
    })
  ])

type type = z.infer<typeof schema>

const createOptionSchema = (z_type: z.ZodType) => (
    z.union([
        z.object({
            is_some: z.literal(false),
            value: z.union([z.null(), z.undefined()])
        }),
        z.object({
            is_some: z.literal(true),
            value: z_type
        })
    ])
)

const ex_schema = createOptionSchema(z.string().min(5))
type ex_type = z.infer<typeof ex_schema>