import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { clearToken, fetchMe, type Me } from "../api/auth";

type AuthContextValue = {
  user: Me | null;
  loading: boolean;
  refresh: () => Promise<void>;
  setUser: React.Dispatch<React.SetStateAction<Me | null>>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<Me | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const refresh = async () => {
    setLoading(true);
    const me = await fetchMe();
    if (!me) {
      clearToken();
      setUser(null);
    } else {
      setUser(me);
    }
    setLoading(false);
  };

  useEffect(() => {
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const value = useMemo(() => ({ user, setUser, loading, refresh }), [user, loading]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
