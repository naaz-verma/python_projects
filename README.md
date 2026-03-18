# WorldWithWeb - Python Project Showcase

> "Don't learn to code. Code to learn."

Welcome to WorldWithWeb's Python learning track! 7 projects across different interest areas -- students pick what excites them, and learn Python through building real things.

---

## The Projects

| # | Project | What You'll Build | Interest Area | Difficulty |
|---|---------|-------------------|---------------|------------|
| 1 | [AI Quiz Master](01_quiz_master/) | AI-powered quiz app on any topic | General + AI | Beginner |
| 2 | [Space Defender](02_space_defender/) | A real playable space shooter game | Gaming | Beginner-Intermediate |
| 3 | [Password Fortress](03_password_fortress/) | Password security analyzer & cracker simulator | Cybersecurity | Intermediate |
| 4 | [AI Story Forge](04_ai_story_forge/) | Choose-your-own-adventure with AI-generated art | AI + Creative | Intermediate-Advanced |
| 5 | [Network Sentinel](05_network_sentinel/) | Network security monitoring dashboard | Cybersecurity | Advanced |
| 6 | [AI Chatbot](06_ai_chatbot/) | Chatbot with swappable personalities (Pirate, Shakespeare, etc.) | AI + Fun | Beginner |
| 7 | [AI Tutor](07_ai_tutor/) | Socratic-method AI tutor for any subject | AI + Education | Beginner-Intermediate |

---

## Quick Start

### 1. Install Python
Download from [python.org](https://www.python.org/downloads/) (version 3.10 or higher)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Key (for AI projects: 1, 4, 6, 7)
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Get your key at: https://platform.openai.com/api-keys
```

### 4. Run a Project
```bash
# Streamlit projects (1, 3, 4, 5, 6, 7)
cd 01_quiz_master
streamlit run app.py

# Pygame project (2)
cd 02_space_defender
python main.py
```

---

## 45-Day Course Structure

Students don't do ALL projects. Based on their interest, they follow a **track** and pick 3-4 projects. Everyone learns full Python fundamentals along the way.

### Week 1-2: Python Foundations (All Students)
Everyone starts here -- core Python through hands-on exercises.
- Variables, data types, strings, numbers
- Lists, dictionaries, sets
- If/elif/else, for loops, while loops
- Functions, parameters, return values
- **Starter Project:** Project 1 (AI Quiz Master) -- everyone builds this together

### Week 3-4: Choose Your Track
Students pick their interest and build 1-2 projects from their track:

| Track | Projects | Python Concepts |
|-------|----------|-----------------|
| **AI & Creativity** | 4 (Story Forge), 6 (Chatbot), 7 (Tutor) | APIs, prompt engineering, state management |
| **Gaming** | 2 (Space Defender) | Classes, objects, game loops, OOP |
| **Cybersecurity** | 3 (Password Fortress), 5 (Network Sentinel) | Hashing, regex, sockets, threading |

### Week 5-6: Polish & Present
- Add personal touches to their project
- Prepare demo presentation
- Present to peers and parents

### After 45 Days: Keep Coming Back
Students who finish the course can:
- Build new features on their projects
- Move to the next difficulty level
- Start the "Beyond Python" track (see Career Tracks below)
- Mentor newer students

---

## Project-Interest Mapping

Not sure which projects to assign? Match the student:

| Student Interest | Recommended Projects | Why |
|-----------------|---------------------|-----|
| "I love AI / ChatGPT" | 1 + 6 + 7 | Builds real AI apps, learns prompt engineering |
| "I want to make games" | 1 + 2 | Learns OOP through game development |
| "I want to be a hacker" | 1 + 3 + 5 | Builds real security tools, understands attacks |
| "I like stories / art" | 1 + 4 | Creative AI with story generation + DALL-E art |
| "I want to build apps" | 1 + 6 + 3 | Web apps with Streamlit, API integration |
| "I'm not sure yet" | 1 + 7 + 2 | Broad exposure across AI, gaming, and learning |

---

## Career Tracks at WorldWithWeb

### Track 1: Programming & Development
```
Python Fundamentals --> These Projects --> Web Development --> Specialization
                                           (React, Node.js)   (Full-Stack, Mobile, Cloud)
```

### Track 2: Hacking & Cybersecurity
```
Python Fundamentals --> Linux --> Networking --> Cloud --> Security
                        (Kali,    (TCP/IP,      (AWS,     (Pen Testing,
                         Bash)     Wireshark)    Azure)    Bug Bounty)
```

### Track 3: Game Development
```
Python + Pygame --> Game Design --> Godot Engine --> Unity/Unreal --> Portfolio
                    (Mechanics,     (GDScript,       (C#/C++,        (Game Jams,
                     Level Design)   2D & 3D)        3D Games)       itch.io)
```

### Track 4: AI & Machine Learning
```
Python + AI APIs --> Data Science --> ML Fundamentals --> Deep Learning --> AI Products
                     (Pandas,         (scikit-learn,      (PyTorch,        (AI SaaS,
                      Plotly)          Regression)         NLP, Vision)     Agents)
```

---

## About WorldWithWeb

We help school students (8th-12th grade) discover and build their tech career -- starting with excitement, ending with expertise.

**Website:** [worldwithweb.com](https://worldwithweb.com)

pip install streamlit google-generativeai python-dotenv plotly pandas pygame

pip install streamlit google-generativeai python-dotenv plotly pandas pygame
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: streamlit in c:\users\asus\appdata\roaming\python\python314\site-packages (1.55.0)
Collecting google-generativeai
  Downloading google_generativeai-0.8.6-py3-none-any.whl.metadata (3.9 kB)
Requirement already satisfied: python-dotenv in c:\users\asus\appdata\roaming\python\python314\site-packages (1.2.2)
Requirement already satisfied: plotly in c:\users\asus\appdata\roaming\python\python314\site-packages (6.6.0)
Requirement already satisfied: pandas in c:\users\asus\appdata\roaming\python\python314\site-packages (2.3.3)       
Collecting pygame
  Using cached pygame-2.6.1.tar.gz (14.8 MB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... error
  error: subprocess-exited-with-error

  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> [112 lines of output]
      Skipping Cython compilation


      WARNING, No "Setup" File Exists, Running "buildconfig/config.py"
      Using WINDOWS configuration...

      Making dir :prebuilt_downloads:
      Downloading... https://www.libsdl.org/release/SDL2-devel-2.28.4-VC.zip 25ef9d201ce3fd5f976c37dddedac36bd173975c
      Unzipping :prebuilt_downloads\SDL2-devel-2.28.4-VC.zip:
      Downloading... https://www.libsdl.org/projects/SDL_image/release/SDL2_image-devel-2.0.5-VC.zip 137f86474691f4e12e76e07d58d5920c8d844d5b
      Unzipping :prebuilt_downloads\SDL2_image-devel-2.0.5-VC.zip:
      Downloading... https://github.com/libsdl-org/SDL_ttf/releases/download/release-2.20.1/SDL2_ttf-devel-2.20.1-VC.zip 371606aceba450384428fd2852f73d2f6290b136
      Unzipping :prebuilt_downloads\SDL2_ttf-devel-2.20.1-VC.zip:
      Downloading... https://github.com/libsdl-org/SDL_mixer/releases/download/release-2.6.2/SDL2_mixer-devel-2.6.2-VC.zip 000e3ea8a50261d46dbd200fb450b93c59ed4482
      Unzipping :prebuilt_downloads\SDL2_mixer-devel-2.6.2-VC.zip:
      Downloading... https://github.com/pygame/pygame/releases/download/2.1.3.dev4/prebuilt-x64-pygame-2.1.4-20220319.zip 16b46596744ce9ef80e7e40fa72ddbafef1cf586
      Unzipping :prebuilt_downloads\prebuilt-x64-pygame-2.1.4-20220319.zip:
      copying into .\prebuilt-x64
      Path for SDL: prebuilt-x64\SDL2-2.28.4
      ...Library directory for SDL: prebuilt-x64/SDL2-2.28.4/lib/x64
      ...Include directory for SDL: prebuilt-x64/SDL2-2.28.4/include
      Path for FONT: prebuilt-x64\SDL2_ttf-2.20.1
      ...Library directory for FONT: prebuilt-x64/SDL2_ttf-2.20.1/lib/x64
      ...Include directory for FONT: prebuilt-x64/SDL2_ttf-2.20.1/include
      Path for IMAGE: prebuilt-x64\SDL2_image-2.0.5
      ...Library directory for IMAGE: prebuilt-x64/SDL2_image-2.0.5/lib/x64
      ...Include directory for IMAGE: prebuilt-x64/SDL2_image-2.0.5/include
      Path for MIXER: prebuilt-x64\SDL2_mixer-2.6.2
      ...Library directory for MIXER: prebuilt-x64/SDL2_mixer-2.6.2/lib/x64
      ...Include directory for MIXER: prebuilt-x64/SDL2_mixer-2.6.2/include
      Path for PORTMIDI: prebuilt-x64
      ...Library directory for PORTMIDI: prebuilt-x64/lib
      ...Include directory for PORTMIDI: prebuilt-x64/include
      DLL for SDL2: prebuilt-x64/SDL2-2.28.4/lib/x64/SDL2.dll
      DLL for SDL2_ttf: prebuilt-x64/SDL2_ttf-2.20.1/lib/x64/SDL2_ttf.dll
      DLL for SDL2_image: prebuilt-x64/SDL2_image-2.0.5/lib/x64/SDL2_image.dll
      DLL for SDL2_mixer: prebuilt-x64/SDL2_mixer-2.6.2/lib/x64/SDL2_mixer.dll
      DLL for portmidi: prebuilt-x64/lib/portmidi.dll
      Path for FREETYPE: prebuilt-x64
      ...Library directory for FREETYPE: prebuilt-x64/lib
      ...Include directory for FREETYPE: prebuilt-x64/include
      Path for PNG not found.
      ...Found include dir but no library dir in prebuilt-x64.
      Path for JPEG not found.
      ...Found include dir but no library dir in prebuilt-x64.
      DLL for freetype: prebuilt-x64/lib/freetype.dll
      DLL for png: prebuilt-x64/SDL2_image-2.0.5/lib/x64/libpng16-16.dll

      ---
      For help with compilation see:
          https://www.pygame.org/wiki/CompileWindows
      To contribute to pygame development see:
          https://www.pygame.org/contribute.html
      ---

      Traceback (most recent call last):
        File "C:\Users\ASUS\AppData\Local\Temp\pip-install-760zmce1\pygame_a1c70613631f4119962989c7a8e61e61\buildconfig\vstools.py", line 4, in <module>
          from distutils.msvccompiler import MSVCCompiler, get_build_architecture
      ModuleNotFoundError: No module named 'distutils.msvccompiler'

      During handling of the above exception, another exception occurred:

      Traceback (most recent call last):
        File "C:\Users\ASUS\AppData\Local\Temp\pip-install-760zmce1\pygame_a1c70613631f4119962989c7a8e61e61\buildconfig\config_win.py", line 336, in configure
          from . import vstools
        File "C:\Users\ASUS\AppData\Local\Temp\pip-install-760zmce1\pygame_a1c70613631f4119962989c7a8e61e61\buildconfig\vstools.py", line 6, in <module>
          from setuptools._distutils.msvccompiler import MSVCCompiler, get_build_architecture
      ModuleNotFoundError: No module named 'setuptools._distutils.msvccompiler'

      During handling of the above exception, another exception occurred:

      Traceback (most recent call last):
        File "C:\Users\ASUS\AppData\Local\Temp\pip-install-760zmce1\pygame_a1c70613631f4119962989c7a8e61e61\buildconfig\vstools.py", line 4, in <module>
          from distutils.msvccompiler import MSVCCompiler, get_build_architecture
      ModuleNotFoundError: No module named 'distutils.msvccompiler'

      During handling of the above exception, another exception occurred:

      Traceback (most recent call last):
        File "C:\Python314\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py", line 389, in <module>
          main()
          ~~~~^^
        File "C:\Python314\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py", line 373, in main
          json_out["return_val"] = hook(**hook_input["kwargs"])
                                   ~~~~^^^^^^^^^^^^^^^^^^^^^^^^
        File "C:\Python314\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py", line 143, in get_requires_for_build_wheel
          return hook(config_settings)
        File "C:\Users\ASUS\AppData\Local\Temp\pip-build-env-_wi9qt2c\overlay\Lib\site-packages\setuptools\build_meta.py", line 333, in get_requires_for_build_wheel
          return self._get_build_requires(config_settings, requirements=[])
                 ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\ASUS\AppData\Local\Temp\pip-build-env-_wi9qt2c\overlay\Lib\site-packages\setuptools\build_meta.py", line 301, in _get_build_requires
          self.run_setup()
          ~~~~~~~~~~~~~~^^
        File "C:\Users\ASUS\AppData\Local\Temp\pip-build-env-_wi9qt2c\overlay\Lib\site-packages\setuptools\build_meta.py", line 520, in run_setup
          super().run_setup(setup_script=setup_script)
          ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "C:\Users\ASUS\AppData\Local\Temp\pip-build-env-_wi9qt2c\overlay\Lib\site-packages\setuptools\build_meta.py", line 317, in run_setup
          exec(code, locals())
          ~~~~^^^^^^^^^^^^^^^^
        File "<string>", line 432, in <module>
        File "C:\Users\ASUS\AppData\Local\Temp\pip-install-760zmce1\pygame_a1c70613631f4119962989c7a8e61e61\buildconfig\config.py", line 234, in main
          deps = CFG.main(**kwds, auto_config=auto)
        File "C:\Users\ASUS\AppData\Local\Temp\pip-install-760zmce1\pygame_a1c70613631f4119962989c7a8e61e61\buildconfig\config_win.py", line 493, in main
          return setup_prebuilt_sdl2(prebuilt_dir)
        File "C:\Users\ASUS\AppData\Local\Temp\pip-install-760zmce1\pygame_a1c70613631f4119962989c7a8e61e61\buildconfig\config_win.py", line 453, in setup_prebuilt_sdl2
          DEPS.configure()
          ~~~~~~~~~~~~~~^^
        File "C:\Users\ASUS\AppData\Local\Temp\pip-install-760zmce1\pygame_a1c70613631f4119962989c7a8e61e61\buildconfig\config_win.py", line 338, in configure
          from buildconfig import vstools
        File "C:\Users\ASUS\AppData\Local\Temp\pip-install-760zmce1\pygame_a1c70613631f4119962989c7a8e61e61\buildconfig\vstools.py", line 6, in <module>
          from setuptools._distutils.msvccompiler import MSVCCompiler, get_build_architecture
      ModuleNotFoundError: No module named 'setuptools._distutils.msvccompiler'
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.

[notice] A new release of pip is available: 25.2 -> 26.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip
error: subprocess-exited-with-error

× Getting requirements to build wheel did not run successfully.
│ exit code: 1
╰─> See above for output.

note: This error originates from a subprocess, and is likely not a problem with pip.