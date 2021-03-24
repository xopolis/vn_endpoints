# vn_endpoints

**URI:** `127.0.0.1:7001`

**Endpoints:**

- `/phrases`

- `/sentences`

- `/verbnoun`

- `/vn_generation_conjugate`


**Docker endpoint :**
`127.0.0.1:7001/verbnoun`

**Postman-endpoint :**
`x.x.x.x:7001/verbnoun`
---------------------------------------

### input

```json
{
    "text": "Direct, plan, or implement policies, objectives, or activities of organizations or businesses to ensure continuing operations, to maximize returns on investments, or to increase productivity."
}
```

### output

```json
[    {"noun":"policy","noun_phrase":"policy","verb":"implement","verb_phrase":"implement"},
    {"noun":"objective","noun_phrase":"objective","verb":"implement","verb_phrase":"implement"},
    {"noun":"activity","noun_phrase":"activity","verb":"implement","verb_phrase":"implement"},
    {"noun":"operation","noun_phrase":"continue operation","verb":"ensure","verb_phrase":"ensure"},
    {"noun":"return","noun_phrase":"return","verb":"maximize","verb_phrase":"maximize"},
    {"noun":"productivity","noun_phrase":"productivity","verb":"increase","verb_phrase":"increase"}
]
```

**Docker endpoint :**
`127.0.0.1:7001/vn_generation_conjugate`

**Postman-endpoint :**
`x.x.x.x:7001/vn_generation_conjugate`
---------------------------------------

```
### input

```json
{
    "text": "Direct, plan, or implement policies, objectives, or activities of organizations or businesses to ensure continuing operations, to maximize returns on investments, or to increase productivity."
}
```

### output

```json
[
    {"noun":"productivity","noun_phrase":"productivity","verb":"maximize","verb_phrase":"maximize"},
    {"noun":"activity","noun_phrase":"activity","verb":"implement","verb_phrase":"implement"},
    {"noun":"activity","noun_phrase":"activity","verb":"direct","verb_phrase":"direct"},
    {"noun":"policy","noun_phrase":"policy","verb":"plan","verb_phrase":"plan"},
    {"noun":"operation","noun_phrase":"continue operation","verb":"ensure","verb_phrase":"ensure"},
    {"noun":"policy","noun_phrase":"policy","verb":"direct","verb_phrase":"direct"},
    {"noun":"activity","noun_phrase":"activity","verb":"plan","verb_phrase":"plan"},
    {"noun":"policy","noun_phrase":"policy","verb":"implement","verb_phrase":"implement"},
    {"noun":"productivity","noun_phrase":"productivity","verb":"increase","verb_phrase":"increase"},
    {"noun":"objective","noun_phrase":"objective","verb":"plan","verb_phrase":"plan"},
    {"noun":"objective","noun_phrase":"objective","verb":"implement","verb_phrase":"implement"},
    {"noun":"objective","noun_phrase":"objective","verb":"direct","verb_phrase":"direct"}
]
```



**Docker endpoint :**
`127.0.0.1:7001/sentences`

**Postman-endpoint :**
`x.x.x.x:7001/sentences`
---------------------------------------

``` json
{
    "text": "Prepare bylaws approved by elected officials, and ensure that bylaws are enforced. Serve as liaisons between organizations, shareholders, and outside organizations."
}
```

### output

```json
[
    "Prepare bylaws approved by elected officials, and ensure that bylaws are enforced.",
    "Serve as liaisons between organizations, shareholders, and outside organizations."
]
```


**Docker endpoint :**
`127.0.0.1:7001/phrases`

**Postman-endpoint :**
`x.x.x.x:7001/phrases`
---------------------------------------

``` json
{
    "text": "Prepare bylaws approved by elected officials, and ensure that bylaws are enforced. Serve as liaisons between organizations, shareholders, and outside organizations."
}
```