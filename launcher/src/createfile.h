#pragma once

#include <windows.h>
#include <MinHook.h>
#include <cstdlib>
#include <string>
#include <iostream>
#include <filesystem>
#include <cassert>
#include <map>


using CreateFileWFnT = decltype(&CreateFileW);
CreateFileWFnT orig_CreateFileW = NULL;
CreateFileWFnT tgt_CreateFileW = NULL;

// filename => new_filename
std::map<std::wstring, std::wstring> gRedirectFiles = {
    {L"global-metadata.dat", L"global-metadata.dat.chs"},
    {L"data.unity3d", L"data.unity3d.chs"},
};

HANDLE WINAPI hook_CreateFileW(
  LPCWSTR               lpFileName,
  DWORD                 dwDesiredAccess,
  DWORD                 dwShareMode,
  LPSECURITY_ATTRIBUTES lpSecurityAttributes,
  DWORD                 dwCreationDisposition,
  DWORD                 dwFlagsAndAttributes,
  HANDLE                hTemplateFile
) {
    if (lpFileName != nullptr) {
        std::wstring filename_raw(lpFileName);
        std::wcout << "CreateFileW: " << filename_raw << std::endl;
        // MessageBoxW(NULL, lpFileName, L"HOOK", MB_OK);

        auto filename_path = new std::filesystem::path(filename_raw);
        auto filename = filename_path->filename();

        if (!gRedirectFiles.contains(filename)) {
            goto END;
        }

        auto& new_filename = gRedirectFiles.at(filename);
        std::wcout << std::format(L"Found {} read, redirect to {}\n", filename_raw, new_filename);
        filename_path->replace_filename(new_filename);
        lpFileName = filename_path->c_str();
    }

END:
    return orig_CreateFileW(
        lpFileName,
        dwDesiredAccess,
        dwShareMode,
        lpSecurityAttributes,
        dwCreationDisposition,
        dwFlagsAndAttributes,
        hTemplateFile
    );
}


// const char* new_data_unity = "data.unity3d.chs";
// using FSOpenFnT = char __fastcall (int* a1, char* a2);
// uintptr_t tgt_loading = 0x483ed0;
// uintptr_t p_aDataUnity3d_0 = 0x14f7b64;
// FSOpenFnT* orig_loading = nullptr;

// char __fastcall hook_loading(int* a1, char* a2) {
//     DWORD player_base = (DWORD)GetModuleHandleW(L"UnityPlayer.dll");
//     p_aDataUnity3d_0 += player_base;

//     char* buf = new char[255];
//     memset(buf, 0, 255);
//     strcpy(buf, new_data_unity);

//     *(DWORD*)(p_aDataUnity3d_0) = (DWORD)buf;

//     return orig_loading(a1, a2);
// }


namespace CreateFileHook {
    int init() {
        std::cout << "Hooking CreateFileW" << std::endl;
        auto ret = MH_CreateHook(
            (LPVOID)&CreateFileW,
            &hook_CreateFileW,
            (LPVOID*)&orig_CreateFileW);

        if (ret != MH_OK) {
            std::cout << std::format("MH_CreateHook Failed for CreateFileW\n");
            return 1;
        }

        if (MH_EnableHook((LPVOID)&CreateFileW) != MH_OK) {
            std::cout << std::format("MH_EnableHook Failed\n");
            return 1;
        }

        // ===================================================
        // std::cout << "Hooking UnityPlayer.dll" << std::endl;
        // DWORD hDll = (DWORD)LoadLibraryW(L"UnityPlayer.dll");
        // DWORD player_base = (DWORD)GetModuleHandleW(L"UnityPlayer.dll");

        // p_aDataUnity3d_0 += player_base;
        // char* buf = new char[255];
        // memset(buf, 0, 255);
        // strcpy(buf, new_data_unity);

        // *(DWORD*)(p_aDataUnity3d_0) = (DWORD)buf;
        return 0;
    }
}
