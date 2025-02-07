/*
    Fix TypeWriter Effects in Chinese mode
*/
#pragma once
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <format>
#include <windows.h>

#include <MinHook.h>

#include "game_def.h"


System_String_o* new_sep = nullptr;

// FIXME(kuriko): use PatternSearch rather than hardcode RVA
// RVA here
intptr_t System_String_Split = 0x3FFE60;
intptr_t tgt_TypewriterSplitText = 0x1fff73;
intptr_t tgt_DeductionConcatText = 0x1cdb6b;


using SystemStringSplitFnT = void*(void* This, void* sep, int32_t options, void* method);

extern "C" void* new_System_String_Split(System_String_o* This, void* sep, int32_t options, void* method) {
    if (new_sep == nullptr) {
        new_sep = (System_String_o*)malloc(sizeof(System_String_o));
        memcpy(new_sep, sep, sizeof(System_String_o));
        new_sep->fields._firstChar = 0x200B;  // FIXME(kuriko): ZeroWidth Space
    }
    auto* ptr = reinterpret_cast<SystemStringSplitFnT*>(System_String_Split);
    // tail jump
    return ptr(This, new_sep, options, method);
}


void* orig_TypewriterSplitText = nullptr;
void __declspec(naked) hook_TypewriterSplitText() {
    __asm {
        call new_System_String_Split
        jmp orig_TypewriterSplitText
    };
}

void* orig_DeductionTypewriterSplitText = nullptr;
void __declspec(naked) hook_DeductionTypeWriterSplitText() {
    __asm {
        call new_System_String_Split
        jmp orig_DeductionTypewriterSplitText
    };
}

namespace Typewriter {
    int init(DWORD base) {
        System_String_Split += base;
        std::cout << std::format("System_String_Split: {:#x}\n", System_String_Split);

        tgt_TypewriterSplitText += base;
        std::cout << std::format("tgt_TypewriterSplitText: {:#x}\n", tgt_TypewriterSplitText);

        tgt_DeductionConcatText += base;
        std::cout << std::format("tgt_DeductionConcatText: {:#x}\n", tgt_DeductionConcatText);

        auto ret = MH_CreateHook(
            (LPVOID)tgt_TypewriterSplitText,
            &hook_TypewriterSplitText,
            (LPVOID*)&orig_TypewriterSplitText);
        if (ret != MH_OK) {
            std::cout << std::format("MH_CreateHook Failed: {:#x} {}\n", (DWORD)tgt_TypewriterSplitText, (int)ret);
            return 1;
        }

        if (MH_EnableHook((LPVOID)tgt_TypewriterSplitText) != MH_OK) {
            std::cout << std::format("MH_EnableHook Failed\n");
            return 1;
        }

        return 0;
    }
}
