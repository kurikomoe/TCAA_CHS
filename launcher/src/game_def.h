#pragma once

#include <windows.h>
#include <cstdint>
#include <cstddef>

struct __declspec(align(4)) System_String_Fields // sizeof=0x8
{
    int32_t _stringLength;
    uint16_t _firstChar;
    // padding byte
    // padding byte
};

struct System_String_o // sizeof=0x10
{
    void *klass;
    void *monitor;
    System_String_Fields fields;
};

struct TMPro_TMP_Text_o {};
struct UnityEngine_GameObject_o {};
struct UnityEngine_UI_HorizontalLayoutGroup_o {};
struct UnityEngine_Events_UnityEvent_o {};
struct Yarn_Unity_DialogueRunner_o {};
struct System_Collections_IEnumerator_o {};
struct System_Collections_Generic_List_TextLogHistoryEntry__o {};
struct UnityEngine_Color_o {};
struct System_Action_o {};
struct UnityEngine_CanvasGroup_o {};
struct System_Collections_Generic_List_LocalizedLine__o {};
struct System_Collections_Generic_List_int__o {};
struct System_Action_int__o {};
struct UnityEngine_AudioClip_o {};
struct CharacterPortrait_o {};

struct UnityEngine_WaitForSeconds_Fields {
  float m_Seconds;
};
static_assert(sizeof(UnityEngine_WaitForSeconds_Fields) == 4);

struct UnityEngine_WaitForSeconds_o {
  void *klass;
  void *monitor;
  UnityEngine_WaitForSeconds_Fields fields;
};

struct DialogueGUI_Fields {
  char padding[0x2c];
  float typeDelay;
  float pauseDelay;
  float autoPlayDelay;
  float textInstantPlayDelay;
  char padding1[192];
  float skip_time;
  struct UnityEngine_WaitForSeconds_o *slowTextWait;
  struct UnityEngine_WaitForSeconds_o *fastTextWait;
  struct UnityEngine_WaitForSeconds_o *textWait;
  struct UnityEngine_WaitForSeconds_o *slowTextPause;
  struct UnityEngine_WaitForSeconds_o *fastTextPause;
  struct UnityEngine_WaitForSeconds_o *textPause;
  bool noSkip;
  bool uiHidden;
  bool textSizeBig;
  bool direction_held;
};
static_assert(sizeof(DialogueGUI_Fields) == 0x11c);

struct DialogueGUI_o
{
  void *klass;
  void *monitor;
  DialogueGUI_Fields fields;
};

struct __declspec(align(4)) Yarn_Unity_LocalizedLine_Fields
{
  struct System_String_o *TextID;
  struct System_String_array *Substitutions;
  struct System_String_o *RawText;
  struct System_String_array *Metadata;
};

struct Yarn_Unity_LocalizedLine_o
{
  void *klass;
  void *monitor;
  Yarn_Unity_LocalizedLine_Fields fields;
};


struct __declspec(align(4)) DialogueGUI__TypeDialogue_d__90_Fields
{
  int32_t __1__state;
  void *__2__current;
  struct DialogueGUI_o *__4__this;
  void *portrait;
  struct Yarn_Unity_LocalizedLine_o *dialogueLine;
  void *markup;
  bool slow_text;
  bool fast_text;
  bool auto_prog;
  bool _high_5__2;
  bool _demon_5__3;
  struct System_String_o *_dialogue_5__4;
  struct System_Collections_Generic_List_int__o *_pauses_5__5;
  struct System_Collections_Generic_List_int__o *_shakes_5__6;
  int32_t _letter_count_5__7;
  struct UnityEngine_WaitForSeconds_o *_wait_5__8;
  struct UnityEngine_WaitForSeconds_o *_pause_5__9;
  int32_t _i_5__10;
};
static_assert(sizeof(DialogueGUI__TypeDialogue_d__90_Fields) == 0x3c);


struct DialogueGUI__TypeDialogue_d__90_o
{
  void *klass;
  void *monitor;
  DialogueGUI__TypeDialogue_d__90_Fields fields;
};

struct Yarn_Unity_LineView_Fields {
  char padding[0x38];
  float holdTime;
  char padding2[0x4];
  struct Yarn_Unity_LocalizedLine_o *currentLine;
  void *currentStopToken;
};
static_assert(sizeof(Yarn_Unity_LineView_Fields) == 0x48);


struct Yarn_Unity_LineView_o
{
  void *klass;
  void *monitor;
  Yarn_Unity_LineView_Fields fields;
};


struct __declspec(align(4)) Yarn_Unity_LineView__RunLineInternal_d__21_Fields
{
  int32_t __1__state;
  void *__2__current;
  struct Yarn_Unity_LineView_o *__4__this;
  struct Yarn_Unity_LocalizedLine_o *dialogueLine;
  struct System_Action_o *onDialogueLineFinished;
};
static_assert(sizeof(Yarn_Unity_LineView__RunLineInternal_d__21_Fields) == 0x14);


struct Yarn_Unity_LineView__RunLineInternal_d__21_o
{
  void *klass;
  void *monitor;
  Yarn_Unity_LineView__RunLineInternal_d__21_Fields fields;
};

struct __declspec(align(4)) Yarn_Unity_DefaultActions__Wait_d__0_Fields
{
  int32_t __1__state;
  void *__2__current;
  float duration;
};
static_assert(sizeof(Yarn_Unity_DefaultActions__Wait_d__0_Fields) == 0xC);


struct Yarn_Unity_DefaultActions__Wait_d__0_o
{
  void *klass;
  void *monitor;
  Yarn_Unity_DefaultActions__Wait_d__0_Fields fields;
};

struct __declspec(align(4)) DialogueGUI__WaitForProgressInput_d__97_Fields
{
  int32_t __1__state;
  void *__2__current;
  struct DialogueGUI_o *__4__this;
  float _timer_5__2;
};
static_assert(sizeof(DialogueGUI__WaitForProgressInput_d__97_Fields) == 0x10);


struct DialogueGUI__WaitForProgressInput_d__97_o
{
  void *klass;
  void *monitor;
  DialogueGUI__WaitForProgressInput_d__97_Fields fields;
};

struct __declspec(align(4)) Axiom__YarnWait_d__9_Fields {
  int32_t __1__state;
  void *__2__current;
  float time;
};


struct Axiom__YarnWait_d__9_o {
  void *klass;
  void *monitor;
  Axiom__YarnWait_d__9_Fields fields;
};

struct __declspec(align(4)) SFXInstance__Routine_d__7_Fields
{
  int32_t __1__state;
  void *__2__current;
  float time;
  void *__4__this;
};


struct SFXInstance__Routine_d__7_o
{
  void *klass;
  void *monitor;
  SFXInstance__Routine_d__7_Fields fields;
};
