---
date: 2025-11-03 7:00:00
categories:
  - ZetechCTF2025
title: Doo-doo-doo-doo...
tags:
  - reverseengineering
  - dtmf
description: ZetechCTF2025 - Reverse engineering DTMF signal challenge
---

## The Challenge

In this reverse engineering challenge, we need to figure out what kind of input a program needs to print "SUCCESS". We're given a binary file. Time to reverse engineer it and find the flag!

**Quick note:** The decompiled code from IDA Pro uses generic variable names like `v7`, `v11`, `v13`, etc. To make this easier to follow, I've renamed the important variables and functions to more descriptive names (like `audio_stream`, `process_audio`, `check_sequence`) as we go through the analysis.

## Step 1: First Glance at the Code (Static Analysis)

When we first open the C++ file, it looks a bit intimidating. But we don't need to understand every single line. The key is to find the most important parts. Let's focus on the `main` function, as that's where every C++ program begins.

```cpp
int __fastcall main(int argc, const char **argv, const char **envp)
{
  // ...
  // Initializes audio recording. The name "record" is a big hint!
  audio_stream = pa_simple_new(..., "record", ...);
  
  // ...
  do
  {
    // Reads audio from the microphone.
    pa_simple_read(audio_stream, audio_buffer, 0x8000, &error);
    
    // Processes the audio data.
    process_audio((__int64)audio_buffer, (__int64)processed_buffer);
    
    // Checks the result and decides what to do next. This is the key!
    should_continue = check_sequence((__int64)state_buffer, (__int64)processed_buffer, state);
    
    // ...
  }
  while (should_continue); // The loop continues until `check_sequence` returns 0.
  
  // If the loop finishes, we win!
  fwrite("SUCCESS\n", 1u, 8u, stderr);
  // ...
}
```

So what's happening here? The program:
1. **Records audio** from the microphone
2. **Processes** the audio with `process_audio`
3. Uses `check_sequence` to verify if the audio matches what it expects
4. Keeps looping until `check_sequence` returns 0 (false)
5. When the loop finishes, it prints "SUCCESS"

Our job is to figure out what `check_sequence` is looking for!

## Step 2: What is Function `check_sequence` Doing? - The Logic

Looking at `check_sequence`, I noticed it's checking for specific frequencies:

**Low frequencies:** 697, 770, 852, 941 Hz  
**High frequencies:** 1209, 1336, 1477, 1633 Hz

A quick Google search confirmed these are the **standard frequencies for DTMF (Dual-Tone Multi-Frequency) signaling**—the sounds a telephone keypad makes! Perfect! You can check [Wikipedia](https://en.wikipedia.org/wiki/DTMF_signaling) for a DTMF frequency chart with more details.

The program checks for the **strongest high frequency** and the **strongest low frequency** to figure out which "key" is being pressed.

Here's the relevant code from the decompiled function `check_sequence` (renamed from `r`):

```cpp
__int64 __fastcall check_sequence(__int64 a1, __int64 a2)
{
  // ... variable declarations ...
  
  // Check high frequencies
  v4[0] = f(a2, 1209);
  v4[1] = f(a2, 1336);
  v4[2] = f(a2, 1477);
  v4[3] = f(a2, 1633);
  
  // Find strongest high frequency
  v12 = -1;
  v11 = 1.0;
  for ( i = 0; i <= 3; ++i )
  {
    if ( *(double *)&v4[i] > v11 )
    {
      v12 = i;  // This is high_freq_index
      v11 = *(double *)&v4[i];
    }
  }
  
  // Check low frequencies
  v3[0] = f(a2, 697);
  v3[1] = f(a2, 770);
  v3[2] = f(a2, 852);
  v3[3] = f(a2, 941);
  
  // Find strongest low frequency
  v9 = -1;
  v8 = 1.0;
  for ( j = 0; j <= 3; ++j )
  {
    if ( *(double *)&v3[j] > v8 )
    {
      v9 = j;  // This is low_freq_index
      v8 = *(double *)&v3[j];
    }
  }
  
  // ... other checks ...
  
  // The key formula!
  v5 = v12 | (4 * v9);  // This is our tone_code
  
  // ... state machine switch statement ...
  switch ( *(_DWORD *)(a1 + 4) )
  {
    case 0: v6 = v5 == 9; break;
    case 1: v6 = v5 == 5; break;
    case 2: v6 = v5 == 10; break;
    case 3: v6 = v5 == 6; break;
    case 4: v6 = v5 == 9; break;
    case 5: v6 = v5 == 8; break;
    case 6: v6 = v5 == 1; break;
    case 7: v6 = v5 == 13; break;
    case 8: if ( v5 ) return 0xFFFFFFFFLL; return 0;
    // ...
  }
}
```

## Step 3: From Code to Digits - The Decoding Process

Now here's the fun part! How do we get from the code to the actual digits? The secret is in this line:

```cpp
tone_code = high_freq_index | (4 * low_freq_index);
```

This formula creates a unique number (`tone_code`) for each DTMF tone. Let me break it down.

The `|` symbol is the **bitwise OR** operator, not regular addition. In bitwise OR, each bit position is set to 1 if either operand has a 1 in that position. For example:
- `4 | 1 = 5` because:
  - `4` in binary = `100`
  - `1` in binary = `001`
  - `100 | 001 = 101` = `5` in decimal

First, the program finds the **index** (position in the list, starting from 0) of the strongest frequency in each group:

**High Frequencies (Index `high_freq_index`):**
- 1209 Hz → 0
- 1336 Hz → 1
- 1477 Hz → 2
- 1633 Hz → 3

**Low Frequencies (Index `low_freq_index`):**
- 697 Hz → 0
- 770 Hz → 1
- 852 Hz → 2
- 941 Hz → 3

### Working Through an Example

The program's first check requires `tone_code` to be **9**. We need to solve the equation: `high_freq_index | (4 * low_freq_index) = 9`.

Let's try different values for `low_freq_index`:

- If `low_freq_index = 0`, then `4 * 0 = 0`, and `high_freq_index | 0 = high_freq_index`. We'd need `high_freq_index = 9`, but that's not possible (max is 3).
- If `low_freq_index = 1`, then `4 * 1 = 4`, and `high_freq_index | 4 = 9`. This would require `high_freq_index = 5` (since 4 | 5 = 5), but that's not 9.
- If `low_freq_index = 2`, then `4 * 2 = 8`. The equation becomes `high_freq_index | 8 = 9`. This works perfectly if `high_freq_index = 1` (since 8 | 1 = 9)!

So, for the first tone, we need: **Low Index = 2** and **High Index = 1**.

Looking at our lists:
- Low Index 2 → **852 Hz**
- High Index 1 → **1336 Hz**

Finally, checking the DTMF keypad chart, the row for 852 Hz and the column for 1336 Hz intersect at the digit **8**.

Bingo! The first digit is **8**! Once you get this pattern, decoding the rest becomes straightforward.

*Pro tip: If you're feeling lazy, you can always ask your friendly neighborhood AI agent to help map out the remaining states. Just don't tell it I said that! 😉*

## Step 4: The State Machine - Cracking the Code

Turns out `check_sequence` has a `switch` statement that acts as a **state machine**. It needs a specific sequence of tones to advance from one state to the next. Applying the decoding method from Step 3 to each state reveals the full sequence.

Here is the full decoding table:

| State | Required `tone_code` | Decoded `low_freq_index` | Decoded `high_freq_index` | Corresponding Frequencies | Final Digit |
|-------|---------------------|--------------------------|---------------------------|---------------------------|-------------|
| 0 | 9 | 2 | 1 | 852 Hz + 1336 Hz | 8 |
| 1 | 5 | 1 | 1 | 770 Hz + 1336 Hz | 5 |
| 2 | 10 | 2 | 2 | 852 Hz + 1477 Hz | 9 |
| 3 | 6 | 1 | 2 | 770 Hz + 1477 Hz | 6 |
| 4 | 9 | 2 | 1 | 852 Hz + 1336 Hz | 8 |
| 5 | 8 | 2 | 0 | 852 Hz + 1209 Hz | 7 |
| 6 | 1 | 0 | 1 | 697 Hz + 1336 Hz | 2 |
| 7 | 13 | 3 | 1 | 941 Hz + 1336 Hz | 0 |
| 8 | 0 | 0 | 0 | 697 Hz + 1209 Hz | 1 |

### How to Decode Each State

Let me show you one more example to make sure it clicks:

**State 1 requires `tone_code = 5`**

Solving: `high_freq_index | (4 * low_freq_index) = 5`

- If `low_freq_index = 1`, then `4 * 1 = 4`, and `high_freq_index | 4 = 5`. This means `high_freq_index = 1` (since 4 | 1 = 5).
- Low Index 1 → **770 Hz**
- High Index 1 → **1336 Hz**
- DTMF chart: 770 Hz row + 1336 Hz column = **5** ✓

## Step 5: The Solution

The program is waiting for a specific sequence of 9 DTMF tones. The secret code is:

```
859687201
```

## Key Takeaways

This challenge demonstrates several important reverse engineering concepts:

1. **Static Analysis**: Understanding code without running it
2. **DTMF Encoding**: Understanding how telephone keypads encode digits

**Flag:** `ZuH4ckN1ght{859687201}`

**Tools:** IDA Pro

---

