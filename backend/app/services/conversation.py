import json
import uuid
from typing import Dict, Any, List, Optional
from app.db.database import query_db, execute_db

class ConversationManager:
    """
    Manages recommendation session state, conversation history,
    and single-dimension preference modifications ("Change One Thing").
    """
    
    def create_session(self, user_id: str, original_query: str, extracted_prefs: Dict[str, Any]) -> str:
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        execute_db(
            """INSERT INTO recommendation_sessions 
            (id, user_id, original_query, current_preferences_json) 
            VALUES (?, ?, ?, ?)""",
            (session_id, user_id, original_query, json.dumps(extracted_prefs))
        )
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        row = query_db("SELECT * FROM recommendation_sessions WHERE id = ?", (session_id,), one=True)
        if not row:
            return None
        return {
            "id": row["id"],
            "user_id": row["user_id"],
            "original_query": row["original_query"],
            "current_preferences": json.loads(row["current_preferences_json"]),
            "created_at": row["created_at"]
        }

    def apply_change_one_thing(self, session_id: str, change_instruction: str) -> Dict[str, Any]:
        """
        Preserves existing recommendation session state while updating ONLY the target preference dimension.
        """
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found.")

        prefs = session["current_preferences"]
        ci_lower = change_instruction.lower()

        # Target modification mapping
        if "darker" in ci_lower or "more dark" in ci_lower:
            prefs["mood"] = "Dark"
        elif "lighter" in ci_lower or "more uplifting" in ci_lower or "comforting" in ci_lower:
            prefs["mood"] = "Comforting"
        elif "shorter" in ci_lower or "less pages" in ci_lower:
            curr_max = prefs.get("max_pages") or 450
            prefs["max_pages"] = max(200, curr_max - 100)
        elif "longer" in ci_lower or "more pages" in ci_lower:
            curr_max = prefs.get("max_pages") or 300
            prefs["max_pages"] = curr_max + 150
        elif "less romance" in ci_lower or "no romance" in ci_lower:
            prefs["romance_level"] = "Low"
        elif "more romance" in ci_lower:
            prefs["romance_level"] = "High"
        elif "faster" in ci_lower or "faster pacing" in ci_lower:
            prefs["pacing"] = "Fast"
        elif "easier" in ci_lower or "simpler" in ci_lower:
            prefs["complexity"] = "Easy"
        elif "more complex" in ci_lower or "deeper" in ci_lower:
            prefs["complexity"] = "High"

        # Record conversation turn
        turn_id = f"turn_{uuid.uuid4().hex[:12]}"
        assistant_resp = f"Updated your preference: {change_instruction}. Recalculating recommendations..."
        
        execute_db(
            """INSERT INTO conversation_turns 
            (id, session_id, user_message, assistant_response, extracted_preferences_json) 
            VALUES (?, ?, ?, ?, ?)""",
            (turn_id, session_id, change_instruction, assistant_resp, json.dumps(prefs))
        )

        # Save updated preference state
        execute_db(
            "UPDATE recommendation_sessions SET current_preferences_json = ? WHERE id = ?",
            (json.dumps(prefs), session_id)
        )

        return prefs

conversation_manager = ConversationManager()
