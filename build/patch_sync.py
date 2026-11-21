# Lock drive-amplitude updates to cycle boundaries: the frame loop stops at each cycle end
# until the read-back has been processed, so every run is reproducible.
def patch(funcs):
    reps = [
      ("  } else if (R.running) {\n    let budget = Math.max(1, Math.round(spf));\n    while (budget > 0 && R.running) {",
       "  } else if (R.running && !R.wait) {\n    let budget = Math.max(1, Math.round(spf));\n    while (budget > 0 && R.running && !R.wait) {"),
      ("        after.push(encodeCycleEnd(enc, R.cycle));\n        R.cycle++; R.stepInCycle = 0;",
       "        after.push(encodeCycleEnd(enc, R.cycle));\n        R.cycle++; R.stepInCycle = 0; R.wait = true;"),
      ("    if (runId !== R.runId) return;\n    onCycle(",
       "    if (runId !== R.runId) return;\n    R.wait = false;\n    onCycle("),
    ]
    for a,b in reps:
        assert a in funcs, a
        funcs = funcs.replace(a,b)
    return funcs
