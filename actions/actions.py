from typing import List, Dict, Text, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction
from actions.agents import call_llm_for_menu, call_llm_for_order, call_llm_for_intent, call_llm_for_confirmation, call_llm_for_detailed_info
from actions.logger import logger

class ActionProvideMenu(Action):
    def name(self) -> Text:
        return "action_provide_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message['text']
        logger.info(f"Received menu message: {user_message}")
        
        # 调用LLM生成菜单
        menu = call_llm_for_menu(user_message)

        if not menu:
            dispatcher.utter_message(text="对不起，我无法提供菜单信息。")
        else:
            dispatcher.utter_message(text=f"这是我们的菜单：\n{menu}")
        
        return []

class ActionOrderFood(Action):
    def name(self) -> Text:
        return "action_order_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message['text']
        logger.info(f"Received order message: {user_message}")
        
        # 调用LLM处理订餐请求
        llm_response = call_llm_for_order(user_message)
        logger.info(f"Received llm order response: {llm_response}")
    

        if len(llm_response) > 10:
            dispatcher.utter_message(text=llm_response)
        else:
            tracker.slots['dish'] = llm_response
            tracker.slots['quantity'] = 1
            dispatcher.utter_message(text=f"好的，您点的是1份{llm_response}。请问还有其他需要的吗？")
        
        return []

# class ActionOrderFood(Action):
#     def name(self) -> Text:
#         return "action_order_food"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         user_message = tracker.latest_message['text']
#         logger.info(f"Received order message: {user_message}")
        
#         # 调用LLM处理订餐请求
#         llm_response = call_llm_for_order(user_message)
#         logger.info(f"Received llm order response: {llm_response}")
#         dish = llm_response.get('dish')
#         quantity = llm_response.get('quantity')
#         confidence = llm_response.get('confidence')

#         if not dish or not quantity or confidence < 0.5:
#             dispatcher.utter_message(text="对不起，我不确定您的订单。请再说一遍？")
#         else:
#             tracker.slots['dish'] = dish
#             tracker.slots['quantity'] = quantity
#             dispatcher.utter_message(text=f"好的，您点的是{quantity}份{dish}。请问还有其他需要的吗？")
        
#         return []

# class ActionRecognizeIntent(Action):
#     def name(self) -> Text:
#         return "action_recognize_intent"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         user_message = tracker.latest_message['text']
        
#         # 调用LLM分析用户意图
#         llm_response = call_llm_for_intent(user_message)
#         intent = llm_response.get('intent')
#         confidence = llm_response.get('confidence')

#         if confidence < 0.5:
#             dispatcher.utter_message(text="对不起，我不确定您的意图。可以再详细描述一下吗？")
#         else:
#             dispatcher.utter_message(text=f"识别的意图是：{intent}（置信度：{confidence}）")
        
#         return []

class ActionRecognizeIntent(Action):
    def name(self) -> Text:
        return "action_recognize_intent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message['text']
        logger.info(f"Received message: {user_message}")
        
        # 调用LLM分析用户意图
        llm_response = call_llm_for_intent(user_message)
        # 预定义意图列表
        predefined_intents = ["request_menu", "order_food", "confirm_order", "provide_info"]
        
        # 简单的字符匹配确定意图
        intent = "unknown"
        for predefined_intent in predefined_intents:
            if predefined_intent in llm_output:
                intent = predefined_intent
                break

        logger.info(f"Received intent response: {intent}")
        # 根据识别到的意图来触发下一个动作
        if intent == "request_menu":
            return [FollowupAction(name="action_provide_menu")]
        elif intent == "order_food":
            return [FollowupAction(name="action_order_food")]
        elif intent == "confirm_order":
            return [FollowupAction(name="action_confirm_order")]
        else:
            return [FollowupAction(name="action_provide_info")]


class ActionConfirmOrder(Action):
    def name(self) -> Text:
        return "action_confirm_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dish = tracker.get_slot("dish")
        quantity = tracker.get_slot("quantity")
        
        # 通过LLM生成确认信息
        confirmation_message = call_llm_for_confirmation(dish, quantity)
        logger.info(f"Received confirm message: {confirmation_message}")
        
        dispatcher.utter_message(text=confirmation_message)
        return []

class ActionProvideInfo(Action):
    def name(self) -> Text:
        return "action_provide_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message['text']
        logger.info(f"Received provide message: {user_message}")
        
        # 通过LLM处理信息请求
        detailed_info = call_llm_for_detailed_info(user_message)
        
        dispatcher.utter_message(text=detailed_info)
        return []


