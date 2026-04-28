from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import os
from typing import List, Optional
from pydantic import BaseModel, Field


scheme = {
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "小说标题，用于标识和命名这部悬疑小说作品"
    },
    "author": {
      "type": "string",
      "enum": [
        "JackLiu"
      ],
      "default": "JackLiu",
      "description": "小说作者，固定填入 JackLiu"
    },
    "genre": {
      "type": "string",
      "default": "悬疑",
      "description": "小说类型，固定填写为悬疑类型"
    },
    "hook": {
      "type": "string",
      "description": "开篇钩子，用于在开头吸引读者好奇心的事件或悬念描述"
    },
    "mystery": {
      "type": "string",
      "description": "核心谜团，小说的核心悬疑主线，整个故事围绕的核心案件或秘密"
    },
    "foreshadowing": {
      "type": "array",
      "description": "伏笔列表，记录故事中埋下的伏笔，为后续剧情发展做铺垫",
      "items": {
        "type": "object",
        "properties": {
          "chapterNumber": {
            "type": "integer",
            "description": "伏笔出现的章节号"
          },
          "description": {
            "type": "string",
            "description": "伏笔的具体描述"
          },
          "payoffChapter": {
            "type": "integer",
            "description": "伏笔回收的章节号"
          }
        },
        "required": [
          "chapterNumber",
          "description",
          "payoffChapter"
        ]
      }
    },
    "redHerrings": {
      "type": "array",
      "description": "误导线索列表，红鲱鱼式的伪线索，用于干扰读者判断",
      "items": {
        "type": "object",
        "properties": {
          "description": {
            "type": "string",
            "description": "误导线索的描述"
          },
          "introducedIn": {
            "type": "integer",
            "description": "误导线索出现的章节"
          },
          "purpose": {
            "type": "string",
            "description": "设置该误导线索的目的"
          }
        },
        "required": [
          "description",
          "introducedIn",
          "purpose"
        ]
      }
    },
    "characters": {
      "type": "array",
      "description": "人物列表，包含小说中所有重要角色",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "角色姓名"
          },
          "role": {
            "type": "string",
            "enum": [
              "protagonist",
              "detective",
              "victim",
              "suspect",
              "witness",
              "villain",
              "supporting"
            ],
            "description": "角色类型：protagonist-主角, detective-侦探, victim-受害者, suspect-嫌疑人, witness-证人, villain-反派, supporting-配角"
          },
          "age": {
            "type": "integer",
            "description": "角色年龄"
          },
          "description": {
            "type": "string",
            "description": "角色外貌和基本特征的描述"
          },
          "personality": {
            "type": "string",
            "description": "角色性格特点"
          },
          "background": {
            "type": "string",
            "description": "角色背景故事和经历"
          },
          "secrets": {
            "type": "array",
            "description": "角色隐藏的秘密，与悬疑相关的隐藏信息",
            "items": {
              "type": "string",
              "description": "秘密的具体内容"
            }
          },
          "motive": {
            "type": "string",
            "description": "角色动机，如果与案件相关的话"
          },
          "alibi": {
            "type": "object",
            "description": "角色不在场证明",
            "properties": {
              "description": {
                "type": "string",
                "description": "不在场证明的描述"
              },
              "isVerifiable": {
                "type": "boolean",
                "description": "是否可验证"
              }
            },
            "required": [
              "isVerifiable",
              "description"
            ]
          },
          "appearsInChapters": {
            "type": "array",
            "description": "角色出现的章节列表",
            "items": {
              "type": "integer"
            }
          }
        },
        "required": [
          "name",
          "role",
          "description",
          "appearsInChapters",
          "alibi",
          "motive",
          "secrets",
          "background",
          "personality",
          "age"
        ]
      }
    },
    "conflicts": {
      "type": "array",
      "description": "冲突列表，记录故事中的主要矛盾和冲突",
      "items": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "enum": [
              "internal",
              "interpersonal",
              "societal",
              "mystery"
            ],
            "description": "冲突类型：internal-内心冲突, interpersonal-人际冲突, societal-社会冲突, mystery-悬疑冲突"
          },
          "title": {
            "type": "string",
            "description": "冲突的标题或名称"
          },
          "description": {
            "type": "string",
            "description": "冲突的详细描述"
          },
          "parties": {
            "type": "array",
            "description": "涉及的冲突方",
            "items": {
              "type": "string",
              "description": "角色名称"
            }
          },
          "chapters": {
            "type": "array",
            "description": "冲突出现的章节",
            "items": {
              "type": "integer"
            }
          },
          "resolution": {
            "type": "string",
            "description": "冲突的解决方式"
          }
        },
        "required": [
          "type",
          "title",
          "description",
          "resolution",
          "chapters",
          "parties"
        ]
      }
    },
    "plotTwists": {
      "type": "array",
      "description": "剧情反转列表，记录故事中的重大转折点",
      "items": {
        "type": "object",
        "properties": {
          "chapterNumber": {
            "type": "integer",
            "description": "反转发生的章节"
          },
          "description": {
            "type": "string",
            "description": "反转的具体内容"
          },
          "impact": {
            "type": "string",
            "description": "反转对剧情的影响"
          }
        },
        "required": [
          "chapterNumber",
          "description",
          "impact"
        ]
      }
    },
    "climax": {
      "type": "object",
      "description": "高潮部分，故事最紧张的高潮情节",
      "properties": {
        "chapterNumber": {
          "type": "integer",
          "description": "高潮发生的章节"
        },
        "description": {
          "type": "string",
          "description": "高潮情节的描述"
        },
        "revealedTruth": {
          "type": "string",
          "description": "高潮揭示的真相"
        }
      },
      "required": [
        "revealedTruth",
        "description",
        "chapterNumber"
      ]
    },
    "resolution": {
      "type": "string",
      "description": "结局/真相，小说的最终结局和案件真相"
    },
    "totalChapters": {
      "type": "integer",
      "minimum": 10,
      "maximum": 10,
      "description": "小说总章节数，固定为10章"
    },
    "chapters": {
      "type": "array",
      "minItems": 10,
      "maxItems": 10,
      "description": "章节列表，固定包含10个章节对象",
      "items": {
        "type": "object",
        "properties": {
          "chapterNumber": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10,
            "description": "章节编号，范围从1到10"
          },
          "chapterTitle": {
            "type": "string",
            "description": "章节标题"
          },
          "content": {
            "type": "string",
            "description": "章节正文内容"
          },
          "suspenseElements": {
            "type": "array",
            "description": "悬疑元素列表",
            "items": {
              "type": "string"
            }
          },
          "keyClues": {
            "type": "array",
            "description": "关键线索列表",
            "items": {
              "type": "string"
            }
          },
          "dialogues": {
            "type": "array",
            "description": "重要对话列表",
            "items": {
              "type": "object",
              "properties": {
                "speaker": {
                  "type": "string",
                  "description": "说话者姓名"
                },
                "content": {
                  "type": "string",
                  "description": "对话内容"
                },
                "significance": {
                  "type": "string",
                  "description": "对话的重要性或隐藏含义"
                }
              },
              "required": [
                "speaker",
                "content",
                "significance"
              ]
            }
          },
          "sceneSettings": {
            "type": "array",
            "description": "场景设置列表",
            "items": {
              "type": "string"
            }
          }
        },
        "required": [
          "chapterNumber",
          "chapterTitle",
          "content",
          "suspenseElements",
          "keyClues",
          "sceneSettings",
          "dialogues"
        ]
      }
    }
  },
  "required": [
    "title",
    "author",
    "genre",
    "hook",
    "mystery",
    "characters",
    "conflicts",
    "totalChapters",
    "chapters",
    "resolution",
    "redHerrings",
    "foreshadowing",
    "climax",
    "plotTwists"
  ]
}

class Alibi(BaseModel):
    description: str = Field(description="不在场证明的描述")
    isVerifiable: bool = Field(description="是否可验证")


class Character(BaseModel):
    name: str = Field(description="角色姓名")
    role: str = Field(
        description="角色类型：protagonist-主角, detective-侦探, victim-受害者, suspect-嫌疑人, witness-证人, villain-反派, supporting-配角",
        enum=["protagonist", "detective", "victim", "suspect", "witness", "villain", "supporting"]
    )
    age: int = Field(description="角色年龄")
    description: str = Field(description="角色外貌和基本特征的描述")
    personality: str = Field(description="角色性格特点")
    background: str = Field(description="角色背景故事和经历")
    secrets: List[str] = Field(description="角色隐藏的秘密，与悬疑相关的隐藏信息")
    motive: str = Field(description="角色动机，如果与案件相关的话")
    alibi: Alibi = Field(description="角色不在场证明")
    appearsInChapters: List[int] = Field(description="角色出现的章节列表")


class Foreshadowing(BaseModel):
    chapterNumber: int = Field(description="伏笔出现的章节号")
    description: str = Field(description="伏笔的具体描述")
    payoffChapter: int = Field(description="伏笔回收的章节号")


class RedHerring(BaseModel):
    description: str = Field(description="误导线索的描述")
    introducedIn: int = Field(description="误导线索出现的章节")
    purpose: str = Field(description="设置该误导线索的目的")


class Dialogue(BaseModel):
    speaker: str = Field(description="说话者姓名")
    content: str = Field(description="对话内容")
    significance: str = Field(description="对话的重要性或隐藏含义")


class Chapter(BaseModel):
    chapterNumber: int = Field(ge=1, le=10, description="章节编号，范围从1到10")
    chapterTitle: str = Field(description="章节标题")
    content: str = Field(description="章节正文内容")
    suspenseElements: List[str] = Field(description="悬疑元素列表")
    keyClues: List[str] = Field(description="关键线索列表")
    dialogues: List[Dialogue] = Field(description="重要对话列表")
    sceneSettings: List[str] = Field(description="场景设置列表")


class Conflict(BaseModel):
    type: str = Field(
        description="冲突类型：internal-内心冲突, interpersonal-人际冲突, societal-社会冲突, mystery-悬疑冲突",
        enum=["internal", "interpersonal", "societal", "mystery"]
    )
    title: str = Field(description="冲突的标题或名称")
    description: str = Field(description="冲突的详细描述")
    parties: List[str] = Field(description="涉及的冲突方")
    chapters: List[int] = Field(description="冲突出现的章节")
    resolution: str = Field(description="冲突的解决方式")


class PlotTwist(BaseModel):
    chapterNumber: int = Field(description="反转发生的章节")
    description: str = Field(description="反转的具体内容")
    impact: str = Field(description="反转对剧情的影响")


class Climax(BaseModel):
    chapterNumber: int = Field(description="高潮发生的章节")
    description: str = Field(description="高潮情节的描述")
    revealedTruth: str = Field(description="高潮揭示的真相")


class NovelOutline(BaseModel):
    title: str = Field(description="小说标题，用于标识和命名这部悬疑小说作品")
    author: str = Field(default="JackLiu", description="小说作者，固定填入 JackLiu")
    genre: str = Field(default="悬疑", description="小说类型，固定填写为悬疑类型")
    hook: str = Field(description="开篇钩子，用于在开头吸引读者好奇心的事件或悬念描述")
    mystery: str = Field(description="核心谜团，小说的核心悬疑主线，整个故事围绕的核心案件或秘密")
    foreshadowing: List[Foreshadowing] = Field(description="伏笔列表，记录故事中埋下的伏笔，为后续剧情发展做铺垫")
    redHerrings: List[RedHerring] = Field(description="误导线索列表，红鲱鱼式的伪线索，用于干扰读者判断")
    characters: List[Character] = Field(description="人物列表，包含小说中所有重要角色")
    conflicts: List[Conflict] = Field(description="冲突列表，记录故事中的主要矛盾和冲突")
    plotTwists: List[PlotTwist] = Field(description="剧情反转列表，记录故事中的重大转折点")
    climax: Climax = Field(description="高潮部分，故事最紧张的高潮情节")
    resolution: str = Field(description="结局/真相，小说的最终结局和案件真相")
    totalChapters: int = Field(default=10, ge=10, le=10, description="小说总章节数，固定为10章")
    chapters: List[Chapter] = Field(description="章节列表，固定包含10个章节对象")


llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL_NAME"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

structured_llm = llm.with_structured_output(NovelOutline)


def generate_novel(topic: str) -> NovelOutline:
    """
    根据主题生成悬疑小说大纲
    
    Args:
        topic: 小说主题或背景设定
    
    Returns:
        NovelOutline: 结构化的小说大纲对象
    """
    prompt = f"""创作一个完整的悬疑小说大纲：

请确保：
1. 包含至少 4-6 个主要角色，每个角色都有详细的背景和秘密
2. 设计至少 3 个伏笔，并在适当的章节回收
3. 包含至少 2 个误导线索（红鲱鱼）
4. 设计至少 2 个剧情反转
5. 10章内容要有起伏，高潮部分要震撼
6. 每个章节都要有具体的内容、悬疑元素和关键线索
7. 结局要出人意料又在情理之中
"""
    
    result = structured_llm.invoke(prompt)
    return result


if __name__ == "__main__":
    topic = "一座偏僻的古宅中发生的神秘失踪案"
    novel = generate_novel(topic)
    
    print("=" * 60)
    print(f"小说标题：{novel.title}")
    print(f"作者：{novel.author}")
    print(f"类型：{novel.genre}")
    print("=" * 60)
    
    print("\n【开篇钩子】")
    print(novel.hook)
    
    print("\n【核心谜团】")
    print(novel.mystery)
    
    print("\n【人物介绍】")
    for char in novel.characters:
        print(f"\n{char.name} ({char.role}) - {char.age}岁")
        print(f"  描述：{char.description}")
        print(f"  性格：{char.personality}")
        print(f"  背景：{char.background}")
        if char.secrets:
            print(f"  秘密：{', '.join(char.secrets)}")
        print(f"  动机：{char.motive}")
        print(f"  不在场证明：{char.alibi.description} (可验证: {char.alibi.isVerifiable})")
    
    print("\n【章节大纲】")
    for chapter in novel.chapters:
        print(f"\n第{chapter.chapterNumber}章：{chapter.chapterTitle}")
        print(f"  内容：{chapter.content[:200]}...")
        print(f"  悬疑元素：{', '.join(chapter.suspenseElements[:2])}")
        print(f"  关键线索：{', '.join(chapter.keyClues[:2])}")
    
    print("\n【高潮】")
    print(f"章节：第{novel.climax.chapterNumber}章")
    print(f"描述：{novel.climax.description}")
    print(f"揭示的真相：{novel.climax.revealedTruth}")
    
    print("\n【结局】")
    print(novel.resolution)
    
    import json
    print("\n" + "=" * 60)
    print("【结构化 JSON 输出】")
    print("=" * 60)
    print(json.dumps(novel.model_dump(), ensure_ascii=False, indent=2))
